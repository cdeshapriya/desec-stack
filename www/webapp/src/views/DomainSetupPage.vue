<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6">
        <v-card>
          <v-toolbar
              color="primary"
              dark
              flat
          >
            <v-toolbar-title>Setup Instructions for <b>{{ domain }}</b></v-toolbar-title>
          </v-toolbar>

          <v-card-text>
            <domain-setup v-bind="$attrs" :domain="domain"></domain-setup>
          </v-card-text>

        </v-card>
      </v-col>
    </v-row>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="3">
        <v-card>
          <v-card-title><div class="text-h6">Find Help</div></v-card-title>
          <v-card-text>
            In our forum <router-link :to="{name: 'talk'}">talk.desec.io</router-link>, members of the community
            discuss ideas and applications of deSEC. If you have a question, chances are that you may be able to find
            the answer there.
          </v-card-text>
          <v-card-actions>
            <v-btn block outlined :to="{name: 'talk'}">Find Help</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      <v-col cols="12" sm="8" md="3">
        <v-card>
          <v-card-title><div class="text-h6">Keep deSEC Going</div></v-card-title>
          <v-card-text>
            To offer free DNS hosting for everyone, deSEC relies on donations only.
            If you like our service, please consider donating.
          </v-card-text>
          <v-card-actions>
            <v-btn block outlined :to="{name: 'donate'}">Donate</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import DomainSetup from "@/views/DomainSetup.vue";

export default {
  name: 'DomainSetupPage',
  components: { DomainSetup },
  props: {
    domain: {
      type: String,
      required: true,
    },
  }
};
</script>
