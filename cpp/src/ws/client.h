#pragma once

#include "util/WS.h"
#include <external/json.hpp>
#include <string>
#include <vector>

using json = nlohmann::json;

namespace ftx {

class WSClient
{
  public:
    WSClient();

    void on_message(util::WS::OnMessageCB cb);
    void connect();
    std::vector<json> on_open();

    void subscribe_orders(std::string market);
    void subscribe_orderbook(std::string market);
    void subscribe_fills(std::string market);
    void subscribe_trades(std::string market);
    void subscribe_ticker(std::string market);

  private:
    std::vector<std::pair<std::string, std::string>> subscriptions;
    util::WS::OnMessageCB message_cb;
    util::WS ws;
    const std::string uri = "wss://ftx.com/ws/";
    const std::string api_key = "";
    const std::string api_secret = "";
    const std::string subaccount_name = "";
};

}
