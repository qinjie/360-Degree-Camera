import React, { Component } from 'react';
import { View } from 'react-native';
import { Container, Content, Text, Card, Header, Body, Button, Title, CardItem, Icon } from 'native-base';
import { Actions } from 'react-native-router-flux';
import RefeshImage from '../components/RefeshImage';

export default class ShowImagePage extends Component {

  constructor(props) {
    super(props);
  }
  componentWillReceiveProps() {
    alert("MrDAT hhuhu");
  }

  componentDidMount() {
    
  }

  render() {
    //alert(this.props.key_name + " " + this.props.camera_name + " " + this.props.base_url);
    return (
      <Container>
        <Header>
          <Body>
            <Title>Auto Refesh Pano : {this.props.camera_name}</Title>
          </Body>
        </Header>
        <Content padder>
          <RefeshImage id={this.props.id} updateFunc={this.props.updateFunc} camera_name={this.props.camera_name} key_name={this.props.key_name} base_url={this.props.base_url} base64Data={this.props.base64Data} />
        </Content>
      </Container>
    );
  }
}