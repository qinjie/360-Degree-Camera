import React, { Component } from 'react';
import { Router, Scene } from 'react-native-router-flux';
import MainPage from './src/pages/MainPage';
import ShowImagePage from './src/pages/ShowImagePage';
export default class App extends Component {
  render() {
    return (
      <Router>
        <Scene key="root">
          <Scene key="MainPage" component={MainPage} title="360 Degree Image" initial={true} hideNavBar={true}/>
          <Scene key="ShowImagePage" component={ShowImagePage} title="360 Degree Image" hideNavBar={true}/>
        </Scene>
      </Router>
    )
  }
}