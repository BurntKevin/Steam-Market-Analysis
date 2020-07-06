import React from "react";
import Layout from "../components/layout.js";
import MarketOverview from "../components/market_overview";

function Homepage() {
  return (
    <Layout body={<MarketOverview />} />
  );
}

export default Homepage;
