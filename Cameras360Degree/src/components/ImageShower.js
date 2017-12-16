import React, { Component } from 'react';
import { Container, Content, Text, Card, Header, Body, Button, Title, CardItem, List, ListItem } from 'native-base';
import { Image, StyleSheet, Modal, Dimensions, ActivityIndicator } from 'react-native';
import { Actions } from 'react-native-router-flux';
import RNFetchBlob from 'react-native-fetch-blob';
import PropTypes from 'prop-types';

import ImageZoom from 'react-native-image-pan-zoom';

export default class ImageShower extends Component {
	constructor(props) {
		super(props);
		this.state = {
			loading: false,
			base64Data: 'data:image/jpeg;base64,',
		}
		this.new_base64Data = "";
		this.test = false;
		this.props.test = false;
		this.updateData = this.updateData.bind(this);
		//keyname base_url
	}

	componentWillMount() {
		this.fetchImage();
		this.setState({ loading: true });
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
				this.setState({ loading: false });
				console.error(error);
			});
	}

	fetch_base64data_image(url) {
		RNFetchBlob.fetch('GET', url)
			.then((res) => {
				let base64Str = 'data:image/jpeg;base64,' + res.base64();
				this.setState({ base64Data: base64Str });
				const images = [];
				images.push(base64Str);
				this.setState({ images });
				this.setState({ loading: false })
			})
			.catch((errorMessage, statusCode) => {
				// error handling
				this.setState({ loading: false });
			})
	}

	closeViewer() {
		this.setState({
			shown: false,
			curIndex: 0
		})
	}

	updateData(new_base64Data) {
		this.setState({ base64Data: new_base64Data });
	}

	handleOnclick = () => {
		this.setState({ cropWidth: Dimensions.get('window').width, cropHeight: Dimensions.get('window').height });
	}

	render() {
		const {loading} = this.state;
		const width = Dimensions.get('window').width - 60;
		const height = width / 4;
		return (
			<Card>
				<Text noted style={{color: "green"}}>Unit {this.props.camera_name}</Text>
				{ loading ? <ActivityIndicator size="large" color="#0000ff" /> :
					<CardItem>
						<Button dark bordered style={{ width: width, height: height }}
							onPress={() => { Actions.ShowImagePage({ id: this.props.id, updateFunc: this.updateData, camera_name: this.props.camera_name, camera_id: this.props.camera_id, key_name: this.props.key_name, key_prefix: this.props.key_prefix, base_url: this.props.base_url, base64Data: this.state.base64Data }); }}>
							<Image
								style={{ width: width, height: height }}
								source={{ uri: this.state.base64Data }}
							/>
						</Button>
					</CardItem>
				}

			</Card>
		)
	}

}