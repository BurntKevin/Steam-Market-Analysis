import React from 'react';
import Layout from "../components/layout/index";

import ViewItemPriceHistoryAnalysis from "../components/ViewItemPriceHistoryAnalysis"
import ViewItemPriceChartAnalysis from "../components/ViewItemPriceChartAnalysis"

function ViewItemAnalysisPage({ match }) {
  const { item_name } = match.params;

  return (
    <Layout
      body1={<ViewItemPriceChartAnalysis item_name={item_name}/>}
      body2={<ViewItemPriceHistoryAnalysis item_name={item_name}/>}
    />
  );
}

export default ViewItemAnalysisPage;
