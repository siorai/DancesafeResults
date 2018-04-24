<template>
  <div id="app">
    <v-app dark>
      <v-navigation-drawer
        clipped
        fixed
        v-model="drawer"
        app
      >
        <v-list dense>
          <v-list-tile>
            <v-list-tile-action>
              <v-icon>dashboard</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <router-link :to="{name: 'Newsurvey'}">
                <v-list-tile-title>Start New Survey</v-list-tile-title>
              </router-link>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile>
            <v-list-tile-action>
              <v-icon>settings</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>View Event Metrics</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile>
            <v-list-tile-action>
              <v-icon>settings</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <router-link :to="{name: 'Adduser' }">
                <v-list-tile-title>Add User</v-list-tile-title>
              </router-link>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile>
            <v-list-tile-action>
              <v-icon>map</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <router-link :to="{name: 'Addevent' }">
                <v-list-tile-title>Add Event</v-list-tile-title>
              </router-link>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile>
            <v-list-tile-action>
              <v-icon>map</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
                <v-list-tile-title @click="fetchMasterDict">Test Import</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
      </v-navigation-drawer>
      <v-toolbar app fixed clipped-left>
        <v-toolbar-side-icon @click.stop="drawer = !drawer" />
        <v-toolbar-title>Dancesafe Results</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-menu bottom left>
          <v-btn icon slot="activator" dark>
            <v-icon>more_vert</v-icon>
          </v-btn>
          <v-list>
            <v-list-tile v-for="option in masterJSON.endPoints" :key="option.title" :to="{name: option.endpointURL}">
              <v-list-tile-content>
                  <v-list-tile-title>{{ option.title }}</v-list-tile-title>
              </v-list-tile-content>
            </v-list-tile>
          </v-list>
        </v-menu>
      </v-toolbar>
      <div class="col-sm-9">
        <router-view/>
      </div>
    </v-app>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'App',
  component: 'add-user',
  data: () => ({
    options: [
      { title: 'Login' },
      { title: 'Logout' },
      { title: 'New User' },
      { title: 'User Settingsfdsaf' }
    ],
    drawer: null,
    masterJSON: null
  }),
  methods: {
    fetchMasterDict () {
      const path = `http://192.168.4.1:9090/fetch_master_dict`
      axios.get(path)
        .then(response => {
          this.masterJSON = response.data
        })
        .then(
          console.log(this.masterJSON)
        )
        .catch(error => {
          console.log(error)
        })
    }
  },
  props: {
    source: String
  },
  created: function () {
    this.masterJSON = this.fetchMasterDict()
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  background: linear-gradient(to bottom, grey, light-yellow);
  margin-top: 60px;
}
</style>
