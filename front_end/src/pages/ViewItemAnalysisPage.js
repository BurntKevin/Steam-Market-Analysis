import React from "react";
import Layout from "../components/layout/Index";

import ViewItemPriceHistoryAnalysis from "../components/ViewItemPriceHistoryAnalysis";
import ViewItemPriceChartAnalysis from "../components/ViewItemPriceChartAnalysis";

function ViewItemAnalysisPage({ match }) {
  const { item_name } = match.params;

  return (
    <Layout
      body={<ViewItemPriceChartAnalysis item_name={item_name}/>}
      extraBody={<ViewItemPriceHistoryAnalysis item_name={item_name}/>}
    />
  );
}

export default ViewItemAnalysisPage;
