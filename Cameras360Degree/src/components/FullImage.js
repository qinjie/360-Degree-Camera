import React, { Component } from 'react';
import { Container, Content, Text, Card, Header, Body, Button, Title, CardItem, List, ListItem } from 'native-base';
import { Image, StyleSheet, Modal, Dimensions } from 'react-native';
import { Actions } from 'react-native-router-flux';
import RNFetchBlob from 'react-native-fetch-blob';
import PropTypes from 'prop-types';

import ImageZoom from 'react-native-image-pan-zoom';

export default class FullImage extends Component {
	constructor(props) {
		super(props);
		this.state = {
			base64Data: this.props.base64Data,
		}
	}

	render() {
		const width = this.props.width;
		const height = this.props.height;
		return (
			<Card onPress={() => { Actions.pop() }}>
				<ImageZoom
					cropWidth={Dimensions.get('window').width }
					cropHeight={Dimensions.get('window').height - 200}
					imageWidth={width}
					imageHeight={height}
				>
					<Image style={{ width: width, height: height }}
						source={{ uri: this.state.base64Data }} />
					<Button dark bordered
						onPress={() => { Actions.pop() }}>
						<Text>Back</Text>
					</Button>
				</ImageZoom>

			</Card>

		)
	}

}