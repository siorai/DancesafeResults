<template>
  <div id="Adduser">
    <v-layout>
      <v-flex xs12 sm6 offset-sm3>
        <v-card>
          <form>
            <v-card-text>
              <v-container fluid>
                <v-layout row>
                  <v-flex>
                    <v-text-field
                      label="Pick a username"
                      name="username"
                      required
                      dark
                      autocomplete
                    />
                  </v-flex>
                </v-layout>
                <v-layout row>
                  <v-flex>
                    <v-text-field
                      prepend-icon="fa-key fa-lg"
                      name="_password"
                      v-model="password"
                      min="8"
                      required
                      :append-icon="e1 ? 'visibility' : 'visibility_off'"
                      :append-icon-cb="() => (e1 = !e1)"
                      :type="e1 ? 'password' : 'text'"
                      counter
                      single-line
                      dark
                    />
                  </v-flex>
                </v-layout>
                <v-layout row>
                  <v-flex>
                    <v-text-field
                      label="Email"
                      prepend-icon="email"
                      name="email"
                      required
                      single-line
                      dark
                      autocomplete
                    />
                  </v-flex>
                </v-layout>
                <v-layout row>
                  <v-flex>
                    <v-text-field
                      prepend-icon="fa-facebook-official fa-lg"
                      name="facebook"
                      single-line
                      dark
                      autocomplete
                    />
                  </v-flex>
                </v-layout>
                <v-layout row>
                  <v-flex>
                    <v-text-field
                      prepend-icon="fa-instagram fa-lg"
                      name="instagram"
                      single-line
                      dark
                      autocomplete
                    />
                  </v-flex>
                </v-layout>
                <v-layout row>
                  <v-flex>
                    <v-select
                      v-bind:items="masterJSON.chapterList"
                      label="Select Chapter"
                      single-line
                      item-text="name"
                      item-value="name"
                      bottom
                    ></v-select>
                  </v-flex>
                </v-layout>
              </v-container>
            </v-card-text>
            <v-btn @click="submit">submit</v-btn>
          </form>
        </v-card>
      </v-flex>
    </v-layout>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'add-user',
  data: () => ({
    e1: false,
    username: '',
    email: '',
    facebook: '',
    instagram: '',
    chapter: '',
    password: 'Password',
    masterJSON: null
  }),
  methods: {
    submit () {
      this.$validator.validateAll()
    },
    fetchMasterDict () {
      const path = `http://localhost:9090/fetch_master_dict`
      axios.get(path)
        .then(response => {
          this.masterJSON = response.data
        })
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

<style scoped>

</style>
