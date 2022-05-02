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
    <div style={{ backgroundColor: "#264783", padding: 0, margin: 0 }}>
      {/* <GeistProvider style = {{ padding: 0, margin: 0}}> */}
        {/* <CssBaseline /> */}
        <Router style={{padding: 0}}>
          <div style={{ padding: 0, margin: 0, width: '100vw', height:'100vh' }}>
            <Switch >
              {/* <Route exact path="/" component={LandingPage} /> */}
              <Route exact path="/" component={sseRecieverPage}/>
              <Route path="/assistant" component={AssistantPage} />
              <Route path="/shortcuts" component={ShortcutsPage} />
              <Route path="/sse" component={sseRecieverPage} />
            </Switch>
          </div>
        </Router>
      {/* </GeistProvider> */}
    </div>
  );
}

export default App;
