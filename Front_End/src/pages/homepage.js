import React from "react";
import Layout from "../components/layout.js";
import MarketOverview from "../components/market_overview";
import TransactionAmount from "../components/transaction_amount";

function Homepage() {
  return (
    <Layout body={<MarketOverview />} extraBody={<TransactionAmount />} />
  );
}

export default Homepage;
