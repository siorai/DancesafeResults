<template>
  <div id="Adduser">
    <v-layout>
      <v-flex xs12 sm6 offset-sm3>
        <v-card>
          <form>
            <v-card-text>
              <v-container fluid>
                <v-layout row>
                  <v-flex xs4>
                    <v-subheader class="grey--text text--lighten-1">Please enter a user name</v-subheader>
                  </v-flex>
                  <v-flex xs8>
                    <v-text-field
                      name="username"
                      required
                      single-line
                      dark
                      autocomplete
                    />
                  </v-flex>
                </v-layout>
                <v-layout row>
                  <v-flex xs4>
                    <v-subheader class="grey--text text--lighten-1">Select a password</v-subheader>
                  </v-flex>
                  <v-flex xs8>
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
                  <v-flex xs4>
                    <v-subheader class="grey--text text--lighten-1">Your email address</v-subheader>
                  </v-flex>
                  <v-flex xs8>
                    <v-text-field
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
                  <v-flex xs4>
                    <v-subheader class="grey--text text--lighten-1">Facebook</v-subheader>
                  </v-flex>
                  <v-flex xs8>

                    <v-text-field
                      prepend-icon="fa-facebook-official fa-lg"
                      name="facebook"
                      required
                      single-line
                      dark
                      autocomplete
                    />
                  </v-flex>
                </v-layout>
                <v-layout row>
                  <v-flex xs4>
                    <v-subheader class="grey--text text--lighten-1">Instagram</v-subheader>
                  </v-flex>
                  <v-flex xs8>
                    <v-text-field
                      prepend-icon="fa-instagram fa-lg"
                      name="instagram"
                      required
                      single-line
                      dark
                      autocomplete
                    />
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
export default {
  name: 'add-user',
  data: () => ({
    e1: false,
    password: 'Password'
  }),
  methods: {
    submit () {
      this.$validator.validateAll()
    }
  },
  props: {
    source: String
  }
}
</script>

<style scoped>

</style>
