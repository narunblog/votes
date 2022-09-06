import axios from "axios";


const axiosBase = axios.create({
	baseURL: process.env.VUE_APP_API_URL,
	headers: {
		"Content-Type": "application/json",
	},
	responseType: "json",
	timeout: 1000,
});


export { axiosBase };