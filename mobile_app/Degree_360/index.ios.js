/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 * @flow
 */
"use strict";
import React, {Component} from 'react';
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
    AsyncStorage,
    AppState,
    NavigatorIOS,
    NetInfo
} from 'react-native';

const timer = require('react-native-timer');
const time_reload = 1000;
var base_link = 'https://zhileq7qw2.execute-api.ap-southeast-1.amazonaws.com/dev/base64_object/iot-360-camera/camera01.jpg'
var url_link = 'https://zhileq7qw2.execute-api.ap-southeast-1.amazonaws.com/dev/base64_object/iot-360-camera/camera01.jpg'
export class Degree_360 extends Component {
    constructor(props) {
        super(props);
        this.state = {
            base64Data: 'data:image/png;base64,',
            checked: false,
            timestamp: '0',
            timestapRequest: '0',
            time: ''
        }
        this.initViewController()
        this.reloadData = this.reloadData.bind(this)
    }

    onPress = () => {
        timer.setInterval("count", this.reloadData, 5);
    };

    async initViewController() {
        try {
            var timestamp = await AsyncStorage.getItem('@MySuperStore:key')
            if (timestamp != null) {
                if (timestamp !== '0') {
                    if (!isNaN(timestamp)) {
                        url_link = base_link + '?timestamp=' + timestamp
                    } else {

                    }
                }
            }

            console.log(url_link)

            let _this = this
            fetch(url_link)
                .then((response) => response.json(),
                    (error) => console.log(error)).catch((error) => {
                console.error(error);
            })
                .then(async(responseJson) => {
                        if (responseJson !== undefined) {
                            console.log('Just Test', responseJson)
                            if (typeof(responseJson.body) !== 'undefined') {
                                if (typeof(responseJson.body) !== 'undefined') {

                                    _this.setState({base64Data: 'data:image/png;base64,' + responseJson.body})
                                    _this.setState({timestapRequest: responseJson.timestamp})
                                    let timestamp2 = responseJson.timestamp
                                    let timestamp1 = new Date(responseJson.timestamp * 1000)
                                    let dateValues = [
                                        timestamp1.getFullYear(),
                                        timestamp1.getMonth() + 1,
                                        timestamp1.getDate(),
                                        timestamp1.getHours(),
                                        timestamp1.getMinutes(),
                                        timestamp1.getSeconds(),
                                    ]

                                    dateValues[1] = (dateValues[1] < 10 ? '0' : '') + dateValues[1]
                                    dateValues[2] = (dateValues[2] < 10 ? '0' : '') + dateValues[2]
                                    dateValues[3] = (dateValues[3] < 10 ? '0' : '') + dateValues[3]
                                    dateValues[4] = (dateValues[4] < 10 ? '0' : '') + dateValues[4]
                                    dateValues[5] = (dateValues[5] < 10 ? '0' : '') + dateValues[5]

                                    let timeConvert = dateValues[0] + '-' + dateValues[1] + '-' + dateValues[2] +
                                        '   ' + dateValues[3] + ':' + dateValues[4] + ':' + dateValues[5]

                                    _this.setState({time: timeConvert})

                                    //console.log(timestamp.toString())

                                    await AsyncStorage.setItem('@MySuperStore:key', timestamp2.toString())
                                }
                            } else {


                            }
                        }

                    },
                    (error) => console.log(error))
                .catch((error) => {
                    timer.clearInterval("Reload")
                    console.error(error);
                });

        } catch (error) {
            timer.clearInterval("Reload")
            console.error(error);
        }
    }

    async reloadData() {
        try {
            var timestamp = this.state.timestapRequest

            if (timestamp !== '0') {
                if (!isNaN(timestamp)) {
                    url_link = base_link + '?timestamp=' + timestamp
                } else {

                }
            }

            let _this = this

            fetch(url_link)
                .then((response) => response.json(),
                    (error) => console.log(error))
                .then(async(responseJson) => {
                    if (responseJson !== undefined) {
                        if (typeof(responseJson.body) !== 'undefined') {
                            console.log(' No Data', responseJson.body, ' ', responseJson.Message)
                            if (typeof(responseJson.body) != 'undefined') {
                                console.log('No Message', responseJson.Message)
                                let newData = 'data:image/png;base64,' + responseJson.body
                                if (newData == this.state.base64Data) {

                                } else {
                                    console.log('Change Image')
                                    _this.setState({base64Data: 'data:image/png;base64,' + responseJson.body})

                                    _this.setState({timestapRequest: responseJson.timestamp})
                                    let timestamp2 = responseJson.timestamp
                                    let timestamp1 = new Date(responseJson.timestamp * 1000)
                                    let dateValues = [
                                        timestamp1.getFullYear(),
                                        timestamp1.getMonth() + 1,
                                        timestamp1.getDate(),
                                        timestamp1.getHours(),
                                        timestamp1.getMinutes(),
                                        timestamp1.getSeconds(),
                                    ]

                                    dateValues[1] = (dateValues[1] < 10 ? '0' : '') + dateValues[1]
                                    dateValues[2] = (dateValues[2] < 10 ? '0' : '') + dateValues[2]
                                    dateValues[3] = (dateValues[3] < 10 ? '0' : '') + dateValues[3]
                                    dateValues[4] = (dateValues[4] < 10 ? '0' : '') + dateValues[4]
                                    dateValues[5] = (dateValues[5] < 10 ? '0' : '') + dateValues[5]

                                    let timeConvert = dateValues[0] + '-' + dateValues[1] + '-' + dateValues[2] +
                                        '   ' + dateValues[3] + ':' + dateValues[4] + ':' + dateValues[5]

                                    _this.setState({time: timeConvert})

                                    //console.log(timestamp.toString())

                                    await AsyncStorage.setItem('@MySuperStore:key', timestamp2.toString())
                                    this.state.timestamp = timestamp2

                                }

                            }
                        }
                    }

                }, (error) => console.log(error))
                .catch((error) => {
                    timer.clearInterval("Reload")
                    console.error(error);
                });

        } catch (error) {
            timer.clearInterval("Reload")
            console.error(error);
        }
    }


    changeState(checked) {

        this.state.checked = checked
        if (this.state.checked == false) {
            timer.clearInterval("Reload")
        } else {
            timer.setInterval("Reload", this.reloadData, time_reload)
        }
    }

    render() {
        return (
            <View style={styles.container}>
                <View style={{marginTop: 0, backgroundColor: '#2196F3', height: 20}}>
                </View>
                <View style={{
                    marginTop: 0,
                    backgroundColor: '#2196F3',
                    height: 44,
                    alignItems: 'center',
                    justifyContent: 'center'
                }}>
                    <Text style={styles.title}> 360 Degree </Text>
                </View>
                <View style={{
                    flexDirection: 'row', alignItems: 'center', justifyContent: 'center',
                    backgroundColor: '#ffffff', marginTop: 15
                }}>
                    <Text style={styles.instructions}> Refresh </Text>
                    <CheckBox style={{marginLeft: 100}}
                              label=''
                              onChange={(checked) => this.changeState((!checked))}/>
                </View>
                <View
                    style={{flex: 1}}
                >
                    <Text style={{
                        marginTop: 10, marginBottom: 10, justifyContent: 'center', alignItems: 'center',
                        textAlign: 'center', fontWeight: '500'
                    }}>
                        {this.state.time}
                    </Text>
                    <TouchableHighlight
                        underlayColor='#FAFAFA'
                        onPress={this.reloadData}
                        style={{flex: 1}}

                    >
                        <Image style={styles.imageStyle}
                               source={{uri: this.state.base64Data}}>
                        </Image>
                    </TouchableHighlight>
                </View>

            </View>
        );
    }
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        marginBottom: 10,
        backgroundColor: '#FAFAFA'
        // justifyContent: 'center',
        // alignItems: 'center',


    },
    welcome: {
        fontSize: 20,
        textAlign: 'center',
        margin: 10,
    },
    title: {
        textAlign: 'center',
        alignItems: 'center',
        fontSize: 25,
        fontWeight: 'bold',
        justifyContent: 'center',
        color: '#ffffff'
    },
    instructions: {
        textAlign: 'center',
        color: '#333333',
        marginBottom: 5,
        fontSize: 20,
        marginRight: 10
    },
    imageStyle: {
        margin: 10,
        flex: 1,
        resizeMode: 'contain'
    }
});

AppRegistry.registerComponent('Degree_360', () => Degree_360);
