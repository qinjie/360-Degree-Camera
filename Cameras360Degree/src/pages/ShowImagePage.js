import React, { Component } from 'react';
import { View, Image, Dimensions, BackHandler, ActivityIndicator } from 'react-native';
import { Container, Content, Text, Card, Header, Body, Button, Title, CardItem, Icon } from 'native-base';
import { Actions } from 'react-native-router-flux';
import RefeshImage from '../components/RefeshImage';
import RNFetchBlob from 'react-native-fetch-blob';
import PercentCircle from 'react-native-percent-circle';
import ProgressBarClassic from 'react-native-progress-bar-classic';

export default class ShowImagePage extends Component {

  constructor(props) {
    super(props);
    this.state = {
      percent: "loading...",
      base64Data: this.props.base64Data,
      base64Data1: "none",
      base64Data2: "none",
      base64Data3: "none",
      base64Data4: "none",
    }
  }

  onBackFunction = () => {
    this.clearTimer();
    Actions.pop({ refresh: { data: "DATA DATA" } });
    Actions.refresh({ data: this.state.base64Data, id: this.props.id });
  }

  componentDidMount() {
    this.fetchAllImage();
    this.createTimer();
  }

  createTimer() {
    this.clearTimer();
    this.refresh = setInterval(this.fetchAllImage, 10000);
  }

  clearTimer() {
    clearInterval(this.refresh);
  }

  fetchAllImage = () => {
    this.fetchImage(this.props.camera_id, 1);
    this.fetchImage(this.props.camera_id, 2);
    this.fetchImage(this.props.camera_id, 3);
    this.fetchImage(this.props.camera_id, 4);
    this.fetchMontionData();
  }

  fetchMontionData() {
    var base_url = "https://jm307gwsej.execute-api.ap-southeast-1.amazonaws.com/api/" + this.props.camera_id;
    fetch(base_url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    }).then(res => res.json())
      .then(resJson => {
        if (resJson['percent'] === '-1' || resJson['percent'] === -1) {
          this.setState({ percent: -1 })
        } else {
          this.setState({ percent: resJson['percent'] });
        }
      })
  }

  fetchImage(camera_id, camera_number) {
    //alert("MrDat" + this.key_name + " " + this.camera_name + " " + this.base_url + " " );
    //alert(camera_id + " " + camera_number);
    var key_name = this.props.key_prefix + "Cam0" + camera_number + "/cam0" + camera_number + "_als_" + camera_id + ".jpg";
    //alert("Key name : " + key_name);
    var base_url = this.props.base_url;
    fetch(base_url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        key_name: key_name
      })
    })
      .then((response) => response.json())
      .then((responseJson) => {
        this.fetch_base64data_image(responseJson['url'], camera_number);
      })
      .catch((error) => {
        console.error(error);
      });
  }

  fetch_base64data_image(url, camera_number) {
    RNFetchBlob.fetch('GET', url)
      .then((res) => {
        let base64Str = 'data:image/jpeg;base64,' + res.base64();
        //alert("Done 1 image");
        //console.log(base64Str);
        switch (camera_number) {
          case 1:
            this.setState({ base64Data1: base64Str });
            break;
          case 2:
            this.setState({ base64Data2: base64Str });
            break;
          case 3:
            this.setState({ base64Data3: base64Str });
            break;
          case 4:
            this.setState({ base64Data4: base64Str });
            break;
          default:
            break;
        }

      })
      .catch((errorMessage, statusCode) => {
        // error handling
      })
  }

  updateFunc = (new_base64Data_pano) => {
    this.setState({ base64Data: new_base64Data_pano });
  }

  render() {
    //alert(this.props.key_name + " " + this.props.camera_name + " " + this.props.base_url);
    const width = Dimensions.get('window').width / 2 - 40;
    const height = width * 4 / 5;
    return (
      <Container>
        <View style={{ flexDirection: 'row', }}>
          <Button color={"#FFFFFF"} style={{ borderRadius: 0 }}
            onPress={() => { this.clearTimer(); Actions.pop({ refresh: { data: "DATA DATA" } }); Actions.refresh({ data: this.state.base64Data, id: this.props.id }); }}>
            <Icon name="arrow-back" />
          </Button>
          <Button style={{ width: Dimensions.get('window').width, borderRadius: 0 }}>
            <Text>Unit {this.props.camera_name} Detail</Text>
          </Button>
        </View>
        <Content padder>
          <Text>Pano : </Text>
          <RefeshImage id={this.props.id} updateFunc={this.updateFunc} camera_name={this.props.camera_name} key_name={this.props.key_name} base_url={this.props.base_url} base64Data={this.props.base64Data} />
          <View>
            <View style={{ flexDirection: 'row' }} >
              <View style={{ justifyContent: 'center', paddingLeft: 20 }}>
                <Text>Camera 1:</Text>

                <Button dark bordered style={{ width: width, height: height, flex: 1, justifyContent: 'center' }} onPress={() => { Actions.FullImage({ base64Data: this.state.base64Data1, width: width * 2, height: height * 2 }); }}>
                  {this.state.base64Data1.length > 50 ?
                    <Image
                      style={{ width: width, height: height }}
                      source={{ uri: this.state.base64Data1 }}
                    /> : <ActivityIndicator size="small" color="#00ff00" />
                  }
                </Button>

              </View>

              <View style={{ justifyContent: 'center', paddingLeft: 20, }}>
                <Text>Camera 2:</Text>
                <Button dark bordered style={{ width: width, height: height, flex: 1, justifyContent: 'center' }} onPress={() => { Actions.FullImage({ base64Data: this.state.base64Data2, width: width * 2, height: height * 2 }); }}>
                  {this.state.base64Data2.length > 50 ?
                    <Image
                      style={{ width: width, height: height }}
                      source={{ uri: this.state.base64Data2 }}
                    /> : <ActivityIndicator size="small" color="#00ff00" />
                  }
                </Button>
              </View>
            </View>

            <View style={{ flexDirection: 'row' }} >
              <View style={{ justifyContent: 'center', paddingLeft: 20 }}>
                <Text>Camera 3:</Text>
                <Button dark bordered style={{ width: width, height: height, flex: 1, justifyContent: 'center' }} onPress={() => { Actions.FullImage({ base64Data: this.state.base64Data3, width: width * 2, height: height * 2 }); }}>
                  {this.state.base64Data3.length > 50 ?
                    <Image
                      style={{ width: width, height: height }}
                      source={{ uri: this.state.base64Data3 }}
                    /> : <ActivityIndicator size="small" color="#00ff00" />
                  }
                </Button>
              </View>

              <View style={{ justifyContent: 'center', paddingLeft: 20, }}>
                <Text>Camera 4:</Text>
                <Button dark bordered style={{ width: width, height: height, flex: 1, justifyContent: 'center' }} onPress={() => { Actions.FullImage({ base64Data: this.state.base64Data4, width: width * 2, height: height * 2 }); }}>
                  {this.state.base64Data4.length > 50 ?
                    <Image
                      style={{ width: width, height: height }}
                      source={{ uri: this.state.base64Data4 }}
                    /> : <ActivityIndicator size="small" color="#00ff00" />
                  }
                </Button>
              </View>
            </View>
            {this.state.percent !== -1 ?
              <View >
                <View style={{ flexDirection: 'row' }}>
                  <Text> Montion: </Text>
                  {
                    this.state.percent === "loading..." ?
                    <ActivityIndicator size="small" color="#00ff00" />
                    : <Text> {parseFloat(this.state.percent).toFixed(2)} %</Text>
                  }
                </View>
                <View>
                  <ProgressBarClassic progress={parseFloat(parseFloat(this.state.percent).toFixed(2))} valueStyle={'none'} />
                </View>
              </View>
              :
              <Text style={{ color: "red" }}>No data</Text>
            }
          </View>
        </Content>
      </Container>
    );
  }
}