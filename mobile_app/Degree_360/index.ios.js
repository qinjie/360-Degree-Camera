/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 * @flow
 */
"use strict";
import React, { Component } from 'react';
import CheckBox from 'react-native-checkbox';
import {
  AppRegistry,
  StyleSheet,
  Text,
  View,
  Image,
  button,
  Alert,
  TouchableHighlight
} from 'react-native';

const timer = require('react-native-timer');
const time_reload = 4000;
const url_link = 'http://172.17.40.212:81/english_contest2/demo_services.php'

export default class Degree_360 extends Component {
  constructor(props){
    super(props);
    this.state = {uri: 'https://www.gravatar.com/avatar/a2d818d801ce38a33807f68fdd92043a?s=64&d=identicon&r=PG',
                checked : false
              }
  }

  onPress = () => {
    timer.setInterval("count", this.reloadData, 5);
  };

  reloadData = () => {
      try {
        fetch(url_link)
          .then((response) => response.json()).catch( (error) => {
            console.error(error);
          })
          .then((responseJson) => {
            console.log(responseJson.url)
              this.setState({uri: responseJson.url})
          })
          .catch((error) => {
            console.error(error);
          });
      } catch(error) {
          console.error(error);
      }
  }


  changeState(checked) {
    console.log(checked)
      this.state.checked = checked
      if (this.state.checked == false) {
          timer.clearInterval("Reload")
      } else {
        timer.setInterval("Reload",this.reloadData,time_reload)
      }
  }

  render() {

    return (
      <View style={styles.container}>
            <View style={{flexDirection : 'row', alignItems: 'center', justifyContent: 'center',
          backgroundColor: '#ffffff'}}>
                <Text style={styles.instructions}> Refresh </Text>
                <CheckBox style={{marginLeft : 100}}
                          label = ''
                          onChange = {(checked) => this.changeState((!checked))}
                          />
            </View>

            <TouchableHighlight
                onPress = {this.reloadData}
                style = {{flex : 1}} >
                <Image style = {styles.imageStyle}
                    source = {{uri : this.state.uri}}>
                </Image>
            </TouchableHighlight>


      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    marginTop: 64,
    flex: 1,
    // justifyContent: 'center',
    // alignItems: 'center',
    marginBottom: 10
  },
  welcome: {
    fontSize: 20,
    textAlign: 'center',
    margin: 10,
  },
  instructions: {
    textAlign: 'center',
    color: '#333333',
    marginBottom: 5,
    fontSize: 30,
    marginRight : 10
  },
  imageStyle: {
    margin : 10,
    flex: 1,
    resizeMode : 'contain'
  }
});

AppRegistry.registerComponent('Degree_360', () => Degree_360);
