<template>
  <div id="adduser">
    <v-layout>
      <v-flex xs12 sm6 offset-sm3>
        <form>
          <v-card-text>
            <v-container fluid>
              <v-layout row>
                <v-flex xs4>
                  <v-subheader class="grey--text text--lighten-1">Event name</v-subheader>
                </v-flex>
                <v-flex xs8>
                  <v-text-field
                    name="eventname"
                    required
                    single-line
                    dark
                    autocomplete
                  />
                </v-flex>
              </v-layout>
              <v-layout row>
                <v-flex xs4>
                  <v-subheader class="grey--text text--lighten-1">Year</v-subheader>
                </v-flex>
                <v-flex xs8>
                  <v-text-field
                    name=""
                    />
                </v-flex>
              </v-layout>
            </v-container>
          </v-card-text>
        </form>
      </v-flex>
    </v-layout>
  </div>
</template>

<script>
export default {
  name: 'add-event'
}
</script>

<style scoped>

</style>
