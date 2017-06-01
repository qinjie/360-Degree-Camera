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
  TouchableHighlight,
  AsyncStorage
} from 'react-native';

const timer = require('react-native-timer');
const time_reload = 4000;
var url_link = 'https://zhileq7qw2.execute-api.ap-southeast-1.amazonaws.com/dev/base64_object/iot-360-camera/camera01.jpg'
export default class Degree_360 extends Component {
  constructor(props){
    super(props);
    this.state = {base64Data: 'data:image/png;base64,',
                checked : false,
                timestamp: -1
              }
  }

  onPress = () => {
    timer.setInterval("count", this.reloadData, 5);
  };

  reloadData = () => {
      try {
        var timestamp =  AsyncStorage.getItem("timestamp")
        console.log(timestamp);
        if (!isNaN(timestamp)) {
          console.log('Not nil')
          url_link = url_link + '?timestamp=' + timestamp
        } else {

        }
        console.log(url_link)

        fetch(url_link)
          .then((response) => response.json()).catch( (error) => {
            console.error(error);
          })
          .then((responseJson) => {
            if (responseJson.body === undefined) {

            } else
            {
              console.log(responseJson.body)
                this.setState({base64Data: this.state.base64Data + responseJson.body})
                let timestamp = responseJson.timestamp
                AsyncStorage.setItem("timestamp", timestamp.toString())
                this.state.timestamp = timestamp
            }
          })
          .catch((error) => {
            timer.clearInterval("Reload")
            console.error(error);
          });

      } catch(error) {
        timer.clearInterval("Reload")
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
    this.reloadData()
    return (
      <View style={styles.containe}>
            <View style = {{marginTop: 20, backgroundColor: '#FAFAFA', height: 44, alignItems: 'center'}}>
                <Text style = {styles.title}> 360 Degree </Text>
            </View>
            <View style={{flexDirection : 'row', alignItems: 'center', justifyContent: 'center',
          backgroundColor: '#ffffff', marginTop: 15}}>
                <Text style={styles.instructions}> Refresh </Text>
                <CheckBox style={{marginLeft : 100}}
                          label = ''
                          onChange = {(checked) => this.changeState((!checked))}
                          />
            </View>

            <TouchableHighlight
                onPress = {this.reloadData}
                style = {{flex : 1}}

                >
                <Image style = {styles.imageStyle}
                    source = {{uri : this.state.base64Data}}>
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
  title: {
    textAlign: 'center',
    alignItems: 'center',
    fontSize: 25
  },
  instructions: {
    textAlign: 'center',
    color: '#333333',
    marginBottom: 5,
    fontSize: 20,
    marginRight : 10
  },
  imageStyle: {
    margin : 10,
    flex: 1,
    resizeMode : 'contain'
  }
});

AppRegistry.registerComponent('Degree_360', () => Degree_360);
