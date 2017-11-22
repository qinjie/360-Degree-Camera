import React, { Component } from 'react';
import { Icon, Container, Content, Text, Card, Header, Body, Button, Title, CardItem, List, ListItem } from 'native-base';
import { Image, StyleSheet } from 'react-native';
import { Actions } from 'react-native-router-flux';
import RNFetchBlob from 'react-native-fetch-blob';

export default class RefeshImage extends Component {
	constructor(props) {
		super(props);
		this.state = {
			status: false,
			base64Data: this.props.base64Data
		}
		//keyname base_url
	}

	componentWillMount() {
		//this.fetchImage();
	}

	fetchImage() {
		var key_name = this.props.key_name;
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
		return (
			// <Image
			// 	style={{ width: 400, height: 100 }}
			// 	source={{ uri: this.state.base64Data }}
			// />
			// <Card>
			

			// 	<CardItem>
			// 		<Image style={{ resizeMode: 'cover' }} source={{ uri: this.state.base64Data }}/>
			// 	</CardItem>

			// 	<CardItem>
			// 		<Icon name={'ios-musical-notes'} style={{ color: '#ED4A6A' }} />
			// 		<Text>Listen now</Text>
			// 	</CardItem>
			// </Card>
			<Card>
				<Button dark bordered style={{ width: 360, height: 80 }} >
					<Image
						style={{ width: 360, height: 75 }}
						source={{ uri: this.state.base64Data }}
					/>
				</Button>
			</Card>
		)
	}

}