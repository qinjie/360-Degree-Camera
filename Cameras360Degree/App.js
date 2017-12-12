import React, { Component } from 'react';
import { Router, Scene, Actions } from 'react-native-router-flux';
import MainPage from './src/pages/MainPage';
import ShowImagePage from './src/pages/ShowImagePage';
import FullImage from './src/components/FullImage';

export default class App extends Component {

  render() {
    return (
      <Router>
        <Scene key="root">
          <Scene key="MainPage" component={MainPage} title="360 Degree Image" initial={true} hideNavBar={true} />
          <Scene key="ShowImagePage" ref={"sip"} component={ShowImagePage} hideNavBar={true} title="360 Degree Image" />
          <Scene key="FullImage" component={FullImage} title="Image Detail" />
        </Scene>
      </Router>
    )
  }
}