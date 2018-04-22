<template>
  <div id="Newsurvey">
    <v-layout>
      <v-flex xs12 sm6 offset-sm3>
        <v-card>
          <v-form method="post" action="http://192.168.4.1:9090/api/add_sample" id="nativeForm">
            <v-card-text>
              <v-container fluid>
                <v-layout row>
                  <v-flex>
                    <v-select
                      v-bind:items="eventList"
                      label="Event"
                      name="eventid"
                      v-model="eventid"
                      item-text="name"
                      item-value="id"
                      required
                      dark
                    />
                  </v-flex>
                </v-layout>
                <v-layout row>
                  <v-flex>
                    <v-select
                      v-bind:items="userList"
                      v-model="shiftLead"
                      label="Shiftlead"
                      name="shiftLead"
                      item-text="name"
                      item-value="id"
                      required
                    ></v-select>
                  </v-flex>
                </v-layout>
                <v-layout row>
                  <v-flex>
                    <v-select
                      v-bind:items="userList"
                      v-model="tester"
                      label="Tester"
                      name="tester"
                      item-text="name"
                      item-value="id"
                      bottom
                      required
                    ></v-select>
                  </v-flex>
                </v-layout>
                <v-layout row>
                  <v-flex>
                    <v-select
                      v-bind:items="userList"
                      v-model="recorder"
                      label="Recorder"
                      name="recorder"
                      item-text="name"
                      item-value="id"
                      bottom
                      required
                    ></v-select>
                  </v-flex>
                </v-layout>
                <v-layout row>
                  <v-flex>
                    <v-select
                      v-bind:items="typesList"
                      v-model="typeid"
                      label="Physical Medium"
                      name="typeid"
                      item-text="name"
                      item-value="id"
                      bottom
                      required
                    ></v-select>
                  </v-flex>
                </v-layout>
                <v-layout row>
                  <v-flex>
                    <v-select
                      v-bind:items="substancesList"
                      v-model="initialSuspect"
                      label="Initially Suspected As"
                      name="initialSuspect"
                      item-text="name"
                      item-value="id"
                      bottom
                      required
                    ></v-select>
                  </v-flex>
                </v-layout>
                <v-layout>
                  <v-flex>
                    <v-text-field
                      label="Physical Description"
                      v-model="description"
                      name="description"
                      multi-line
                    ></v-text-field>
                  </v-flex>
                </v-layout>
                <v-layout row>
                  <v-flex xs6>
                    <v-checkbox
                      label="Groundscore?"
                      v-model="groundscore"
                    ></v-checkbox>
                  </v-flex>
                  <v-flex xs6>
                    <v-checkbox
                      label="Conclusive Result?"
                      v-model="conclusiveResult"
                    ></v-checkbox>
                  </v-flex>
                </v-layout>
                <v-layout row>
                  <v-flex>
                    <v-select
                      v-bind:items="substancesList"
                      v-model="finalConclusion"
                      label="Final Conclusion"
                      name="finalConclusion"
                      item-text="name"
                      item-value="id"
                      bottom
                      required
                    ></v-select>
                  </v-flex>
                </v-layout>
                <v-layout row>
                  <v-flex xs6>
                    <v-select
                      v-bind:items="acquiredPlan"
                      v-model="acquiredOnSite"
                      label="Acquired on site?"
                      name="acquiredOnSite"
                      item-text="text"
                      item-value="value"
                      required
                    ></v-select>
                  </v-flex>
                  <v-flex xs6>
                    <v-select
                      v-bind:items="acquiredPlan"
                      v-model="planToIngest"
                      label="Plan To Ingest?"
                      name="planToIngest"
                      item-text="text"
                      item-value="value"
                      required
                    ></v-select>
                  </v-flex>
                </v-layout>
              </v-container>
            </v-card-text>
            <v-btn @click="submit">submit</v-btn>
          </v-form>
        </v-card>
      </v-flex>
    </v-layout>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'add-event',
  data: () => ({
    el: false,
    userList: null,
    eventList: null,
    typesList: null,
    substancesList: null,
    eventid: '',
    shiftLead: '',
    tester: '',
    recorder: '',
    typeid: '',
    initialSuspect: '',
    description: '',
    groundscore: false,
    conclusiveResult: true,
    finalConclusion: '',
    acquiredPlan: [
      { text: 'Yes', value: 'yes' },
      { text: 'No', value: 'no' },
      { text: 'Didnt Ask', value: 'didntask' },
      { text: 'Declined', value: 'declined' }
    ],
    acquiredOnSite: '',
    planToIngest: ''
  }),
  methods: {
    fetchSubstances () {
      const path = `http://192.168.4.1:9090/api/fetch_substances`
      axios.get(path)
        .then(response => {
          this.substancesList = response.data
        })
        .catch(error => {
          console.log(error)
        })
    },
    fetchTypes () {
      const path = `http://192.168.4.1:9090/api/fetch_types`
      axios.get(path)
        .then(response => {
          this.typesList = response.data
        })
        .catch(error => {
          console.log(error)
        })
    },
    fetchEvents () {
      const path = `http://192.168.4.1:9090/api/fetch_events`
      axios.get(path)
        .then(response => {
          this.eventList = response.data
        })
        .catch(error => {
          console.log(error)
        })
    },
    fetchUsers () {
      const path = `http://192.168.4.1:9090/api/fetch_users`
      axios.get(path)
        .then(response => {
          this.userList = response.data
        })
        .catch(error => {
          console.log(error)
        })
    },
    submit () {
      axios.post('http://192.168.4.1:9090/api/add_sample', {
        eventid: this.eventid,
        shiftLead: this.shiftLead,
        tester: this.tester,
        recorder: this.recorder,
        typeid: this.typeid,
        initialSuspect: this.initialSuspect,
        description: this.description,
        groundscore: this.groundscore,
        conclusiveResult: this.conclusiveResult,
        finalConclusion: this.finalConclusion,
        acquiredOnSite: this.acquiredOnSite,
        planToIngest: this.planToIngest
      })
    }
  },
  created: function () {
    this.userList = this.fetchUsers()
    this.eventList = this.fetchEvents()
    this.typesList = this.fetchTypes()
    this.substancesList = this.fetchSubstances()
  }
}
</script>

<style scoped>

</style>
