#include "ws/client.h"
#include <external/json.hpp>
#include <iostream>

using json = nlohmann::json;


int main()
{
    ftx::WSClient client;
    client.subscribe_orders("BTC-PERP");
    client.subscribe_orderbook("BTC-PERP");
    client.subscribe_ticker("BTC-PERP");

    client.on_message([](json j) { std::cout << "msg: " << j << "\n"; });

    client.connect();
}
