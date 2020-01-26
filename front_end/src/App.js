// Standard Libraries
import React from 'react'
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

// Pages
import ViewAllGamesPage from "./pages/ViewAllGamesPage";
import ViewAllItemsPage from "./pages/ViewAllItemsPage";
import ViewItemDetailsPage from "./pages/ViewItemDetailsPage";

function App() {
  return (
    <Router>
      <Switch>
        <Route exact path="/" component={ViewAllGamesPage} />
        <Route exact path="/view_all_items:game" component={ViewAllItemsPage} />
        <Route exact path="/view_item_details:item" component={ViewItemDetailsPage} />
      </Switch>
    </Router>
  );
}

export default App;
