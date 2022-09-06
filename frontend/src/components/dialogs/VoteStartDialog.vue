<template>
  <v-row justify="center">
    <v-dialog
      v-model="dialog"
      persistent
      max-width="600px"
    >
      <v-card>
        <v-card-title>
          <span class="text-h5">投票作成</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col
                cols="12">
                <v-text-field
                  v-model="formData.title"
                  :counter="100"
                  label="タイトル"
                  required
                  prepend-icon="mdi-format-title"
                ></v-text-field>
              </v-col>
              <v-col
                cols="12"
                sm="6"
                md="6">
                <v-menu
                  v-model="menu1"
                  :close-on-content-click="false"
                  :nudge-right="40"
                  transition="scale-transition"
                  offset-y
                  min-width="auto">
                  <template v-slot:activator="{ on, attrs }">
                    <v-text-field
                      v-model="formData.startDate"
                      label="開始日"
                      prepend-icon="mdi-calendar"
                      readonly
                      v-bind="attrs"
                      v-on="on">
                    </v-text-field>
                  </template>
                  <v-date-picker
                    v-model="formData.startDate"
                    @input="menu1 = false"
                    locale="ja"
                    no-title
                    color="primary"
                    :day-format="date => new Date(date).getDate()">
                  </v-date-picker>
                </v-menu>
              </v-col>
              <v-col
                cols="12"
                sm="6"
                md="6">
                <v-select
                  v-model="formData.startTime"
                  :items="timeSelector()"
                  :rules="[v => !!v || 'Item is required']"
                  label="時間"
                  required>
                </v-select>
              </v-col>
              <v-col
                cols="12"
                sm="6"
                md="6">
                <v-menu
                  v-model="menu2"
                  :close-on-content-click="false"
                  :nudge-right="40"
                  transition="scale-transition"
                  offset-y
                  min-width="auto">
                  <template v-slot:activator="{ on, attrs }">
                    <v-text-field
                      v-model="formData.endDate"
                      label="終了日"
                      prepend-icon="mdi-calendar"
                      readonly
                      v-bind="attrs"
                      v-on="on">
                    </v-text-field>
                  </template>
                  <v-date-picker
                    v-model="formData.endDate"
                    @input="menu2 = false"
                    locale="ja"
                    no-title
                    color="primary"
                    :day-format="date => new Date(date).getDate()">
                  </v-date-picker>
                </v-menu>
              </v-col>
              <v-col
                cols="12"
                sm="6"
                md="6">
                <v-select
                  v-model="formData.endTime"
                  :items="timeSelector()"
                  :rules="[v => !!v || 'Item is required']"
                  label="時間"
                  required>
                </v-select>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            text
            @click="$emit('onClickClose',formData)"
          >
            Close
          </v-btn>
          <v-btn
            color="primary"
            text
            @click="$emit('onClickSave',formData)"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>


<script>
  export default {
    name: 'VoteStartDialog',
  data: () => ({
    formData: {
        startDate: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
        startTime: false,
        endDate: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
        endTime: false,
        title: "",
      },
      menu1: false,
      menu2: false,
    }),
    methods: {
      timeSelector(options) {
        // 初期値の設定
        options = options || {};
        if(options.startTime == null) options.startTime = [0,0];
        if(options.endTime == null) options.endTime = [23, 59];
        if(options.stepTime == null) options.stepTime = 15;

        const startTime = options.startTime
        const endTime = options.endTime
        const stepTime = options.stepTime
        let items = []
        let untilTime =  new Date(Date.now())
        untilTime.setHours(endTime[0])
        untilTime.setMinutes(endTime[1])
        let fromTime = new Date(Date.now())
        fromTime.setHours(startTime[0])
        fromTime.setMinutes(startTime[1])
        let hour = startTime[0]
        let minute = startTime[1]
        while (fromTime < untilTime) {
          const item = `${hour}:${String(minute).padStart(2, '0')}`
          items.push(item)

          minute = minute + stepTime
          if (minute >= 60) {
            hour ++
            minute = minute - 60
          }
          fromTime.setHours(hour)
          fromTime.setMinutes(minute)
        }
        return items
      },
    },
      props: {
        dialog: false,
      },
    }
</script>