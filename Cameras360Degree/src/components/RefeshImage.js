import React, { Component } from 'react';
import { Icon, Container, Content, Text, Card, Header, Body, Button, Title, CardItem, List, ListItem } from 'native-base';
import { Image, StyleSheet, Dimensions } from 'react-native';
import { Actions } from 'react-native-router-flux';
import RNFetchBlob from 'react-native-fetch-blob';

export default class RefeshImage extends Component {
	constructor(props) {
		super(props);
		this.state = {
			status: false,
			base64Data: this.props.base64Data
		}
		this.key_name = this.props.key_name;
		this.base_url = this.props.base_url;
		this.camare_name = this.props.camera_name;
		this.fetchImage = this.fetchImage.bind(this);
		//alert("MrDat" + this.props.key_name + " " + this.props.camera_name + " " + this.props.base_url);
		//keyname base_url
	}

	componentDidMount() {
		//this.fetchImage();
		//this.props.update();	
		this.createTimer();
	}

	createTimer() {
		this.clearTimer();
		//alert("Created Timer");
		this.refesh = setInterval(this.fetchImage, 10000);
	}

	clearTimer() {
		//alert("Clear Timer");
		clearInterval(this.refesh);
	}

	fetchImage() {
		//alert("MrDat" + this.key_name + " " + this.camera_name + " " + this.base_url);
		var key_name = this.key_name;
		var base_url = this.base_url;
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
				this.fetch_base64data_image(responseJson['url']);
			})
			.catch((error) => {
				console.error(error);
			});
	}

	fetch_base64data_image(url) {
		RNFetchBlob.fetch('GET', url)
			.then((res) => {
				let base64Str = 'data:image/jpeg;base64,' + res.base64();
				this.setState({ base64Data: base64Str });
			})
			.catch((errorMessage, statusCode) => {
				// error handling
			})
	}

	render() {
		const width = Dimensions.get('window').width - 20;
		const height = width / 4;
		return (
			<Card>
				<Button onPress={() => { Actions.FullImage({ base64Data: this.state.base64Data, width: width, height: height }); }} dark bordered style={{ width: 360, height: 80 }} >
					<Image
						style={{ width: width, height: height }}
						source={{ uri: this.state.base64Data }}
					/>
				</Button>
			</Card>
		)
	}

}