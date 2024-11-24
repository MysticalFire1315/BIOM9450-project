<template>
    <v-card
        prepend-icon="mdi-account"
        title="User Profile"
      >
        <v-card-text>
          <v-row dense>
            <v-col
              cols="12"
              md="4"
              sm="6"
            >
              <v-text-field
                hint = "First Name of the Patient"
                label="First name*"
                required
              ></v-text-field>
            </v-col>

            <v-col
              cols="12"
              md="4"
              sm="6"
            >
              <v-text-field
                hint="Last Name of the Patient"
                label="Last name*"
                required
              ></v-text-field>
            </v-col>

            <v-col
              cols="12"
              md="4"
              sm="6"
            >
              <v-avatar>
                <v-icon icon="mdi-account-circle"></v-icon>
              </v-avatar>
              <v-btn class="text-caption text-medium-emphasis">
                Clear
              </v-btn>
            </v-col>

            <v-col
              cols="12"
              md="9"
              sm="6"
            >
              <v-text-field
                label="Address*"
                required
              ></v-text-field>
            </v-col>

            <v-col
              cols="12"
              md="3"
              sm="6"
            >
              <v-text-field
                label="Country"
                required
              ></v-text-field>
            </v-col>

            <v-col
              cols="12"
              md="6"
              sm="6"
            >
              <v-text-field
                label="Emergency Contact Name"
                required
              ></v-text-field>
            </v-col>

            <v-col
              cols="12"
              md="6"
              sm="6"
            >
              <v-text-field
                label="Emergency Contact Phone"
                required
              ></v-text-field>
            </v-col>


            <v-col
              cols="12"
              sm="6"
            >
              <v-select
                :items="['Male', 'Female', 'Other']"
                label="Gender*"
                required
              ></v-select>
            </v-col>

            <v-col
              cols="12"
              sm="6"
            >
            <v-text-field
                hint = "Please enter the date of birth following the format YYYY-MM-DD"
                label="Date of Birth"
                required
              ></v-text-field>
            </v-col>
          </v-row>

          <small class="text-caption text-medium-emphasis">*indicates required field</small>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn
            text="Close"
            variant="plain"
          ></v-btn>

          <v-btn
            color="primary"
            text="Save"
            variant="tonal"
          ></v-btn>
        </v-card-actions>
      </v-card>
</template>