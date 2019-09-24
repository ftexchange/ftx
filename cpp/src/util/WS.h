#pragma once

#include <external/json.hpp>
#include <functional>
#include <websocketpp/client.hpp>
#include <websocketpp/config/asio_client.hpp>

using json = nlohmann::json;

namespace util {

class WS
{
  public:
    using WSClient = websocketpp::client<websocketpp::config::asio_tls_client>;
    using OnOpenCB = std::function<std::vector<json>()>;
    using OnMessageCB = std::function<void(json j)>;

    WS();
    void configure(std::string _uri,
                   std::string _api_key,
                   std::string _api_secret,
                   std::string _subaccount_name);
    void set_on_open_cb(OnOpenCB open_cb);
    void set_on_message_cb(OnMessageCB message_cb);
    void connect();

  private:
    WSClient wsclient;
    WSClient::connection_ptr connection;
    OnOpenCB on_open_cb;
    OnMessageCB on_message_cb;
    std::string uri;
    std::string api_key;
    std::string api_secret;
    std::string subaccount_name;
};

}
