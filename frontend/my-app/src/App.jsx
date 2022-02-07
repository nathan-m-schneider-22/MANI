import "./App.css";
import React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import AssistantPage from "./containers/assistantPage/AssistantPage";
import LandingPage from "./containers/landingPage/LandingPage";
import ShortcutsPage from "./containers/shortcutsPage/ShortcutsPage";
import { GeistProvider, CssBaseline, Page } from "@geist-ui/react";
import sseRecieverPage from "./containers/sseRecieverPage/sseRecieverPage";

function App() {
  return (
    <div style={{ backgroundColor: "#a8b4fc" }}>
      <GeistProvider>
        <CssBaseline />
        <Router>
          <Page className="geist" style={{ paddingTop: 0 }}>
            <Switch>
              <Route exact path="/" component={LandingPage} />
              <Route path="/assistant" component={AssistantPage} />
              <Route path="/shortcuts" component={ShortcutsPage} />
              <Route path="/sse" component={sseRecieverPage} />
            </Switch>
          </Page>
        </Router>
      </GeistProvider>
    </div>
  );
}

export default App;
