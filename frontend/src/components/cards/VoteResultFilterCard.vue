<template>
	<div>
		<v-card
    outlined>
		<v-card-text>
			<v-row>
				<v-col cols="3">
					<v-select
						label="投票"
						v-model="formData.vote"
						:items="votes"
						item-value="id"
						item-text="title"></v-select>
				</v-col>
				<v-col cols="3">
					<v-select
						label="ユーザー"
						v-model="formData.user"
						:items="users"
						item-value="id"
						item-text="email"></v-select>
				</v-col>
				<v-col cols="3" class="d-flex">
					<v-text-field
						type="datetime-local"
						label="期間"
						v-model="formData.startDatetime">
					</v-text-field>
					<span class="align-self-center">〜</span>
					<v-text-field
						type="datetime-local"
						v-model="formData.endDatetime">
					</v-text-field>
				</v-col>
			</v-row>
		</v-card-text>
			<v-card-actions>
				<v-btn
					depressed
					color="primary"
					@click="formActionDone">
					絞り込む
				</v-btn>
				<v-btn
					depressed
					text
					outlined
					@click="formActionCancel">
					条件をクリア
				</v-btn>
			</v-card-actions>
  	</v-card>
	</div>
</template>

<script>
import { axiosAPI } from '@/mixins/AxiosAPI'


  export default {
		data: () => {
			return {
				formData: {
					vote: null,
					user: null,
					startDatetime: null,
					endDatetime: null,
				},
				votes: [],
				users:[],
			}
		},
		props: {},
		components: {},
		methods: {
			formActionDone() {
				this.$emit('formActionDone', this.formData)
				this.initFormData()
			},
			formActionCancel() {
				this.initFormData()
			},
			initFormData() {
				const defaultFormData = {
					vote: null,
					user: null,
					startDatetime: null,
					endDatetime:null,
				}
				this.formData = Object.assign({},defaultFormData)
			},
			getVoteList() {
				const endpoint = '/api/votes/vote/'
				axiosAPI.get(endpoint)
					.then(response => {
						this.votes.push(...response.data)
				})
			},
			getUserList() {
				const endpoint = '/api/votes/user/'
				axiosAPI.get(endpoint)
					.then(response => {
						this.users.push(...response.data)
				})
			}
		},
		created() {
			this.getVoteList()
			this.getUserList()
		},
	}
</script>