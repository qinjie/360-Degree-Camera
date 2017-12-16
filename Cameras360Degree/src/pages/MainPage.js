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
      listCam: [],
      listId: []
    }
    this.my = './src/my.jpg';
    this.base_url = "https://jyf7s0ji3m.execute-api.ap-southeast-1.amazonaws.com/dev/s3_signed_url/download";
    this.key_prefix = "360-degree-camera/";
    this.go_ShowImagePage = this.go_ShowImagePage.bind(this);
    //this.update = this.update.bind(this);
    this.props.test = false;
    this.test = false;
  }

  componentDidMount() {
    this.init_list_camera();
  }

  init_list_camera() {
    //fetch list camera
    var listCamera_name = ['001', '002'];
    var listId = ["1","2"];
    this.setState({ listCam: listCamera_name, listId });
    for (let i = 0; i < this.state.listCam.length; i++) {
      this.fetchImageIndex(i);
    }
  }

  componentWillReceiveProps(nextProps) {
    //console.log("Main" + nextProps.data);
    this.refs[nextProps.id].updateData(nextProps.data);
  }

  go_ShowImagePage(props, i) {
      Actions.ShowImagePage({...props, update: this.update, id: i});
  }

  renderCard() {
    const { listCam, listBase64Data } = this.state;
    const key_prefix = this.key_prefix;
    const base_url = this.base_url;
    if (!listCam) return;
    return listCam.map((camera_name, i) => {
      return <ImageShower key={i} id={i} ref={i} camera_id={this.state.listId[i]} camera_name={camera_name} key_prefix={key_prefix} key_name={key_prefix + 'Pano/pano' + camera_name + '.jpg'} base_url={base_url} />
    })
  }

  render() {
    return (
      <Container>
        <Header>
          <Body>
            <Title>All Units</Title>
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
