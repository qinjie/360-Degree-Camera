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
const onPress = () => {
  timer.setInterval("count", reloadData, 5);
};

const reloadData = () => {
  console.log("5s")
}



export default class Degree_360 extends Component {
  constructor(props){
    super(props);
    this.state = {uri: 'https://www.gravatar.com/avatar/a2d818d801ce38a33807f68fdd92043a?s=64&d=identicon&r=PG',
                checked : false
              }
  }

  getMoviesFromApiAsync() {
/*
    fetch('http://localhost:3000/files')
      .then((response) => response.json())
      .then((responseJson) => {
        if (this.state.checked == true) {
          this.setState({uri: 'https://www.gravatar.com/avatar/a20ba68e4e99f17177cb1303d56036da?s=32&d=identicon&r=PG&f=1'})
        } else {
          this.setState({uri: 'https://www.gravatar.com/avatar/a2d818d801ce38a33807f68fdd92043a?s=64&d=identicon&r=PG'})
        }

        console.log(responseJson[0].image)
      })
      .catch((error) => {
        console.error(error);
      }); */

  }


  changeState(checked) {
    console.log(checked)
      this.state.checked = checked
      if (this.state.checked == false) {
          timer.clearInterval("Reload")
      } else {
        timer.setInterval("Reload",reloadData,1000)
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
                onPress = {reloadData}
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
