import React, { Component } from 'react';
import { Container, Content, Text, Card, Header, Body, Button, Title, CardItem, List, ListItem } from 'native-base';
import { Actions } from 'react-native-router-flux';
import { Image, StyleSheet } from 'react-native';
import RNFetchBlob from 'react-native-fetch-blob';

import ImageShower from "../components/ImageShower";

export default class MainPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      listCam: []
    }
    this.my = './src/my.jpg';
    this.base_url = "https://jyf7s0ji3m.execute-api.ap-southeast-1.amazonaws.com/dev/s3_signed_url/download";
    this.key_prefix = "360-degree-camera/";
  }

  componentWillMount() {
    this.props.base_url = "https://jyf7s0ji3m.execute-api.ap-southeast-1.amazonaws.com/dev/s3_signed_url/download";
    this.props.key_prefix = "360-degree-camera/";
  }

  componentDidMount() {
    this.init_list_camera();
  }

  init_list_camera() {
    //fetch list camera
    var listCamera_name = ['001', '002'];
    this.setState({ listCam: listCamera_name });
    for (let i = 0; i < this.state.listCam.length; i++) {
      this.fetchImageIndex(i);
    }
  }

  renderCard() {
    const { listCam, listBase64Data } = this.state;
    const key_prefix = this.key_prefix;
    const base_url = this.base_url;
    if (!listCam) return;
    return listCam.map((camera_name) => {
      return <ImageShower camera_name={camera_name} key_name={key_prefix + 'Pano/pano' + camera_name + '.jpg'} base_url={base_url} />
    })
  }

  render() {
    return (
      <Container>
        <Header>
          <Body>
            <Title>All camera</Title>
          </Body>
        </Header>
        <Content padder>
          {
            this.renderCard()
          }
        </Content>
      </Container>
    );
  }
}
