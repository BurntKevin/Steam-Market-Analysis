import React from 'react';
import Layout from "../components/layout/index";

import ViewAllGames from "../components/ViewAllGames"

function ViewAllGamesPage() {
  return (
    <Layout
      body={<ViewAllGames />}
    />
  );
}

export default ViewAllGamesPage;
