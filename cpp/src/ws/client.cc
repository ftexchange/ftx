#include "ws/client.h"
#include "util/Encoding.h"
#include "util/Time.h"
#include <utility>

namespace encoding = util::encoding;

namespace ftx {

WSClient::WSClient()
{
    ws.configure(uri, api_key, api_secret, subaccount_name);
    ws.set_on_open_cb([this]() { return this->on_open(); });
}

void WSClient::on_message(util::WS::OnMessageCB cb)
{
    ws.set_on_message_cb(cb);
}

void WSClient::connect()
{
    ws.connect();
}

std::vector<json> WSClient::on_open()
{
    std::vector<json> msgs;

    if (!(api_key.empty() || api_secret.empty())) {
        long ts = util::get_ms_timestamp(util::current_time()).count();
        std::string data = std::to_string(ts) + "websocket_login";
        std::string hmacced = encoding::hmac(std::string(api_secret), data, 32);
        std::string sign =
          encoding::string_to_hex((unsigned char*)hmacced.c_str(), 32);
        json msg = {{"op", "login"},
                    {"args", {{"key", api_key}, {"sign", sign}, {"time", ts}}}};
        if (!subaccount_name.empty()) {
            msg.push_back({"subaccount", subaccount_name});
        }
        msgs.push_back(msg);
    }

    for (auto& [market, channel] : subscriptions) {
        json msg = {
          {"op", "subscribe"}, {"channel", channel}, {"market", market}};
        msgs.push_back(msg);
    }

    return msgs;
}

void WSClient::subscribe_orders(std::string market)
{
    subscriptions.push_back(std::make_pair(market, "orders"));
}

void WSClient::subscribe_orderbook(std::string market)
{
    subscriptions.push_back(std::make_pair(market, "orderbook"));
}

void WSClient::subscribe_fills(std::string market)
{
    subscriptions.push_back(std::make_pair(market, "fills"));
}

void WSClient::subscribe_trades(std::string market)
{
    subscriptions.push_back(std::make_pair(market, "trades"));
}

void WSClient::subscribe_ticker(std::string market)
{
    subscriptions.push_back(std::make_pair(market, "ticker"));
}

}
