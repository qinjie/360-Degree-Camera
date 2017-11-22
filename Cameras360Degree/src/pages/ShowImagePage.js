import React, { Component } from 'react';
import { View } from 'react-native';
import { Container, Content, Text, Card, Header, Body, Button, Title, CardItem, Icon } from 'native-base';
import { Actions } from 'react-native-router-flux';
import RefeshImage from '../components/RefeshImage';

export default class ShowImagePage extends Component {
  render() {
    return (
      <Container>
        <Header>
          <Body>
            <Title>Auto Refesh Camera : {this.props.camera_name}</Title>
          </Body>
        </Header>
        <Content padder>
          <RefeshImage camera_name={this.props.camera_name} key_name={this.props.key_name} base_url={this.props.base_url} base64Data={this.props.base64Data} />
          <Button dark bordered
            onPress={() => { Actions.pop(); }}>
            <Text>Back</Text>
          </Button>
        </Content>
      </Container>
    );
  }
}