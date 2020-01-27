// Standard Libraries
import React from 'react'
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

// Pages
import ViewAllGamesPage from "./pages/ViewAllGamesPage";
import ViewAllItemsPage from "./pages/ViewAllItemsPage";
import ViewItemAnalysisPage from "./pages/ViewItemAnalysisPage";

function App() {
  return (
    <Router>
      <Switch>
        <Route exact path="/" component={ViewAllGamesPage} />
        <Route exact path="/view_all_items:game_id" component={ViewAllItemsPage} />
        <Route exact path="/view_item_analysis:item_name" component={ViewItemAnalysisPage} />
      </Switch>
    </Router>
  );
}

export default App;
