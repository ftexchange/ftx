#pragma once

#include <boost/asio/connect.hpp>
#include <boost/beast/core.hpp>
#include <boost/beast/http.hpp>

#include <string>

namespace beast = boost::beast;
namespace http = beast::http;
namespace net = boost::asio;

namespace util {

class HTTPSession
{

    using Request = http::request<http::string_body>;
    using Response = http::response<http::string_body>;

  public:
    void configure(std::string _uri,
                   std::string _api_key,
                   std::string _api_secret,
                   std::string _subaccount_name);

    http::response<http::string_body> get(const std::string target);
    http::response<http::string_body> post(const std::string target,
                                           const std::string payload);
    http::response<http::string_body> delete_(const std::string target);

  private:
    http::response<http::string_body> request(
      http::request<http::string_body> req);

    void authenticate(http::request<http::string_body>& req);

  private:
    net::io_context ioc;

    std::string uri;
    std::string api_key;
    std::string api_secret;
    std::string subaccount_name;
};
}
