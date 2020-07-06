// Standard Libraries
import React from 'react'
import { BrowserRouter, Route, Switch } from 'react-router-dom';

// Theme
import 'semantic-ui-css/semantic.min.css'

// Pages
import homepage from "./pages/homepage";

function App() {
  return (
    <BrowserRouter>
      <Switch>
        <Route exact path="/" component={homepage} />
      </Switch>
    </BrowserRouter>
  );
}

export default App;
