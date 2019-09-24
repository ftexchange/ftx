#include "util/HTTP.h"
#include "util/Encoding.h"
#include "util/Time.h"

#include <boost/asio/ip/tcp.hpp>
#include <boost/asio/ssl.hpp>
#include <boost/asio/ssl/error.hpp>
#include <boost/asio/ssl/stream.hpp>
#include <boost/beast/version.hpp>

namespace ssl = boost::asio::ssl;
using tcp = net::ip::tcp;

namespace util {

void HTTPSession::configure(std::string _uri,
                            std::string _api_key,
                            std::string _api_secret,
                            std::string _subaccount_name)
{
    uri = _uri;
    api_key = _api_key;
    api_secret = _api_secret;
    subaccount_name = _subaccount_name;
}

http::response<http::string_body> HTTPSession::get(const std::string target)
{
    std::string endpoint = "/api/" + target;
    http::request<http::string_body> req{http::verb::get, endpoint, 11};
    return request(req);
}

http::response<http::string_body> HTTPSession::post(const std::string target,
                                                    const std::string payload)
{
    std::string endpoint = "/api/" + target;
    http::request<http::string_body> req{http::verb::post, endpoint, 11};
    req.body() = payload;
    req.prepare_payload();
    return request(req);
}

http::response<http::string_body> HTTPSession::delete_(const std::string target)
{
    std::string endpoint = "/api/" + target;
    http::request<http::string_body> req{http::verb::delete_, endpoint, 11};
    return request(req);
}

http::response<http::string_body> HTTPSession::request(
  http::request<http::string_body> req)
{
    req.set(http::field::host, uri.c_str());
    req.set(http::field::user_agent, BOOST_BEAST_VERSION_STRING);

    ssl::context ctx{ssl::context::sslv23_client};
    ctx.set_default_verify_paths();

    tcp::resolver resolver{ioc};
    ssl::stream<tcp::socket> stream{ioc, ctx};

    // Set SNI Hostname (many hosts need this to handshake successfully)
    if (!SSL_set_tlsext_host_name(stream.native_handle(), uri.c_str())) {
        boost::system::error_code ec{static_cast<int>(::ERR_get_error()),
                                     net::error::get_ssl_category()};
        throw boost::system::system_error{ec};
    }

    auto const results = resolver.resolve(uri.c_str(), "443");
    net::connect(stream.next_layer(), results.begin(), results.end());
    stream.handshake(ssl::stream_base::client);

    authenticate(req);

    if (req.method() == http::verb::post) {
        req.set(http::field::content_type, "application/json");
    }

    http::write(stream, req);
    boost::beast::flat_buffer buffer;
    http::response<http::string_body> response;
    http::read(stream, buffer, response);

    boost::system::error_code ec;
    stream.shutdown(ec);
    if (ec == boost::asio::error::eof) {
        // Rationale:
        // http://stackoverflow.com/questions/25587403/boost-asio-ssl-async-shutdown-always-finishes-with-an-error
        ec.assign(0, ec.category());
    }

    return response;
}

void HTTPSession::authenticate(http::request<http::string_body>& req)
{

    std::string method(req.method_string());
    std::string path(req.target());
    std::string body(req.body());

    long ts = get_ms_timestamp(current_time()).count();
    std::string data = std::to_string(ts) + method + path;
    if (!body.empty()) {
        data += body;
    }
    std::string hmacced = encoding::hmac(std::string(api_secret), data, 32);
    std::string sign =
      encoding::string_to_hex((unsigned char*)hmacced.c_str(), 32);

    req.set("FTX-KEY", api_key);
    req.set("FTX-TS", ts);
    req.set("FTX-SIGN", sign);
    if (!subaccount_name.empty()) {
        req.set("FTX-SUBACCOUNT", subaccount_name);
    }
}
}
