<template>
  <div id="addevent">
    <v-layout>
      <v-flex xs12 sm6 offset-sm3>
        <v-card>
          <v-form method="post" action="http://192.168.4.1:9090/api/new_event" id="nativeForm">
            <v-card-text>
              <v-container fluid>
                <v-layout row>
                  <v-flex>
                    <v-text-field
                      label="Event Name"
                      name="eventname"
                      v-model="eventname"
                      required
                      dark
                      autocomplete
                    />
                  </v-flex>
                </v-layout>
                <v-layout row>
                  <v-flex>
                    <v-text-field
                      label="Year"
                      name="year"
                      v-model="year"
                      required
                      />
                  </v-flex>
                </v-layout>
                <v-layout row>
                  <v-flex>
                    <v-text-field
                      label="City"
                      name="city"
                      v-model="city"
                      required
                      dark
                      autocomplete
                    />
                  </v-flex>
                </v-layout>
                <v-layout row>
                  <v-flex>
                    <v-text-field
                      label="State"
                      name="state"
                      v-model="state"
                      dark
                      autocomplete
                    />
                  </v-flex>
                </v-layout>
                <v-layout row>
                  <v-flex>
                    <v-text-field
                      label="Region"
                      name="region"
                      v-model="region"
                      dark
                      autocomplete
                    />
                  </v-flex>
                </v-layout>
                <v-layout row>
                  <v-flex>
                    <v-select
                      v-bind:items="userList"
                      v-model="author"
                      label="Select Author"
                      single-line
                      name="author"
                      item-text="name"
                      item-value="id"
                      bottom
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
    eventname: '',
    year: '',
    city: '',
    state: '',
    region: '',
    author: ''
  }),
  methods: {
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
      axios.post('http://192.168.4.1:9090/api/new_event', {
        name: this.eventname,
        year: this.year,
        city: this.city,
        state: this.state,
        region: this.region,
        author: this.author
      })
    }
  },
  created: function () {
    this.userList = this.fetchUsers()
  }
}
</script>

<style scoped>

</style>
