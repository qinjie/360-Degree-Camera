import React, { Component } from 'react';
import { Container, Content, Text, Card, Header, Body, Button, Title, CardItem, List, ListItem } from 'native-base';
import { Image, StyleSheet } from 'react-native';
import { Actions } from 'react-native-router-flux';
import RNFetchBlob from 'react-native-fetch-blob';

export default class ImageShower extends Component {
	constructor(props) {
		super(props);
		this.state = {
			status: false,
			base64Data: 'data:image/jpeg;base64,',
		}
		this.new_base64Data = "";
		this.test = false;
		this.props.test = false;
		this.updateData = this.updateData.bind(this);
		//keyname base_url
	}

	componentWillReceiveProps(nextProps) {
		//alert(nextProps.data);
		//console.log(nextProps);
		//alert("MRDAT" + this.props.test + this.state.test + this.test + test.test);
		//console.log("MrDAt");
		//console.log(test);
		// alert(this.data + "MrDAT" + this.props.data);
		// if (this.new_base64Data != "") {
		// 	alert("update thoi");
		// 	this.setState({ base64Data: this.new_base64Data });
		// }
	}

	componentWillMount() {
		//alert(this.props.key_name + " "  + this.props.base_url);
		this.fetchImage();
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

	updateData(new_base64Data) {
		//alert("Image Shower call back");
		//this.new_base64Data = new_base64Data;
		this.setState({ base64Data: new_base64Data });
	}

	render() {
		return (
			<Card>
				<Text noted>Camera : {this.props.camera_name}</Text>
				<CardItem>
					<Button dark bordered style={{ width: 300, height: 80 }}
						onPress={() => { Actions.ShowImagePage({id:this.props.id, updateFunc: this.updateData, camera_name: this.props.camera_name, key_name: this.props.key_name, base_url: this.props.base_url, base64Data: this.state.base64Data }); }}>
						<Image
							style={{ width: 300, height: 75 }}
							source={{ uri: this.state.base64Data }}
						/>
					</Button>
				</CardItem>
			</Card>
		)
	}

}