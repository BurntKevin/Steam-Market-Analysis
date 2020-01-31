import React from 'react';
import Layout from "../components/layout/index";

import ViewAllItems from "../components/ViewAllItems"

function ViewAllItemsPage({ match }) {
  const { game_id } = match.params;

  return (
    <Layout
      body1={<ViewAllItems game_id={game_id}/>}
    />
  );
}

export default ViewAllItemsPage;
