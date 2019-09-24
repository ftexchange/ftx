#include "rest/client.h"

namespace ftx {

RESTClient::RESTClient()
{
    http_client.configure(uri, api_key, api_secret, subaccount_name);
}

json RESTClient::list_futures()
{
    auto response = http_client.get("futures");
    return json::parse(response.body());
}

json RESTClient::list_markets()
{
    auto response = http_client.get("markets");
    return json::parse(response.body());
}

json RESTClient::get_orderbook(const std::string market, int depth)
{
    auto response =
      http_client.get("markets/" + market + "?depth=" + std::to_string(depth));
    return json::parse(response.body());
}

json RESTClient::get_trades(const std::string market)
{
    auto response = http_client.get("markets/" + market + "/trades");
    return json::parse(response.body());
}

json RESTClient::get_account_info()
{
    auto response = http_client.get("account");
    return json::parse(response.body());
}

json RESTClient::get_open_orders()
{
    auto response = http_client.get("orders");
    return json::parse(response.body());
}

json RESTClient::place_order(const std::string market,
                             const std::string side,
                             double price,
                             double size,
                             bool ioc,
                             bool post_only,
                             bool reduce_only)
{
    json payload = {{"market", market},
                    {"side", side},
                    {"price", price},
                    {"type", "limit"},
                    {"size", size},
                    {"ioc", ioc},
                    {"postOnly", post_only},
                    {"reduceOnly", reduce_only}};
    auto response = http_client.post("orders", payload.dump());
    return json::parse(response.body());
}

json RESTClient::place_order(const std::string market,
                             const std::string side,
                             double size,
                             bool ioc,
                             bool post_only,
                             bool reduce_only)
{
    json payload = {{"market", market},
                    {"side", side},
                    {"price", NULL},
                    {"type", "market"},
                    {"size", size},
                    {"ioc", ioc},
                    {"postOnly", post_only},
                    {"reduceOnly", reduce_only}};
    auto response = http_client.post("orders", payload.dump());
    return json::parse(response.body());
}

json RESTClient::cancel_order(const std::string order_id)
{
    auto response = http_client.delete_("orders/" + order_id);
    return json::parse(response.body());
}

json RESTClient::get_fills()
{
    auto response = http_client.get("fills");
    return json::parse(response.body());
}

json RESTClient::get_balances()
{
    auto response = http_client.get("wallet/balances");
    return json::parse(response.body());
}

json RESTClient::get_deposit_address(const std::string ticker)
{
    auto response = http_client.get("wallet/deposit_address/" + ticker);
    return json::parse(response.body());
}

}
