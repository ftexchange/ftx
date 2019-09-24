#include "util/WS.h"

namespace util {

WS::WS()
{
    wsclient.set_access_channels(websocketpp::log::alevel::none);
    wsclient.set_error_channels(websocketpp::log::elevel::fatal);

    wsclient.init_asio();

    wsclient.set_open_handler([this](websocketpp::connection_hdl hdl) {
        auto subscriptions = on_open_cb();
        for (auto& subscription : subscriptions) {
            wsclient.send(
              hdl, subscription.dump(), websocketpp::frame::opcode::text);
        }
    });

    wsclient.set_message_handler(
      [this](websocketpp::connection_hdl, WSClient::message_ptr msg) {
          json j = msg->get_raw_payload().c_str();
          on_message_cb(j);
      });

    wsclient.set_close_handler([this](websocketpp::connection_hdl) {
        std::cout << "connection closed";
    });

    wsclient.set_interrupt_handler(
      [this](websocketpp::connection_hdl) { throw "Interrupt handler"; });

    wsclient.set_fail_handler(
      [this](websocketpp::connection_hdl) { throw "Fail handler"; });

    wsclient.set_tls_init_handler([](websocketpp::connection_hdl) {
        return websocketpp::lib::make_shared<boost::asio::ssl::context>(
          boost::asio::ssl::context::tlsv12);
    });
}

void WS::configure(std::string _uri,
                   std::string _api_key,
                   std::string _api_secret,
                   std::string _subaccount_name)
{
    uri = _uri;
    api_key = _api_key;
    api_secret = _api_secret;
    subaccount_name = _subaccount_name;
}

void WS::set_on_open_cb(OnOpenCB open_cb)
{
    on_open_cb = open_cb;
}

void WS::set_on_message_cb(OnMessageCB message_cb)
{
    on_message_cb = message_cb;
}

void WS::connect()
{
    websocketpp::lib::error_code ec;
    connection = wsclient.get_connection(uri, ec);
    if (ec) {
        std::string err =
          "Could not create connection because: " + ec.message() + "\n";
        throw err;
    }
    wsclient.connect(connection);
    wsclient.run();
}

}
