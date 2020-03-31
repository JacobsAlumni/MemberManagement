<script lang="ts">
import Vue from "vue";
import Component from 'vue-class-component';

import getCookie from "../../base/utils/cookie";
import {MemberType, MemberTypeDescriptions, MemberTier, getAllowedTiers, MemberTierShortTitles, MemberTierDescriptions} from "../../base/utils/membership";

const emailProviders = [
  "gmail.com",
  "yahoo.com",
  "hotmail.com",
  "gmx.de",
  "web.de",
  "outlook.com",
  "googlemail.com",
  "icloud.com",
  "hotmail.de"
];

// the default birthdaye
const birthDateDefault = new Date();
birthDateDefault.setFullYear(birthDateDefault.getFullYear() - 24);
const birthDateDefaultString = `${birthDateDefault.getFullYear()}-${(birthDateDefault.getMonth() + 1)
        .toString()
        .padStart(2, "0")}-${birthDateDefault
        .getDate()
        .toString()
        .padStart(2, "0")}`;


@Component
export default class SignupForm extends Vue {
  declare $refs: {
    memberType: HTMLInputElement;
  };

  // datea
  showDetailedName = false;
  fullName = "";
  firstNames = "";
  middleNames = "";
  lastNames = "";
  email = "";
  tos = false;
  showEmailSuggestions = false;
  birthDate = birthDateDefaultString;
  accountExists = false;
  alumniemail = "";
  showMembershipType = false;
  memberType = MemberType.Alumnus;
  memberTier = MemberTier.Contributor;
  csrf_token = getCookie('csrftoken')!;

  // computed data
  get emailSuggestions(): string[] {
    const emailParts = this.$data.email.split("@");
    if (!this.email || !emailParts) {
      return [];
    }

    return emailProviders.map(
      providerDomain => emailParts[0] + "@" + providerDomain
    );
  }

  get alumniEmailSuggestions(): string[] {
    const emailParts = this.$data.alumniemail.split("@");
    if (!this.alumniemail || !emailParts) {
      return [];
    }

    return [emailParts[0] + "@jacobs-alumni.de"];
  }

  get tierChoices(): Record<string, string> {
    return getAllowedTiers(this.memberType).reduce<Record<string, string>>((acc, v) => {
      acc[v] = MemberTierShortTitles[v];
      return acc;
    }, {});
  };

  get signUpText(): string {
    return MemberTypeDescriptions[this.memberType];
  }

  //methods
  checkName(event: KeyboardEvent & {target: HTMLInputElement}) {
      const nameParts = event.target?.value.split(" ");

      this.firstNames = nameParts[0];
      this.middleNames = nameParts.slice(1, nameParts.length - 1).join(" ");
      this.lastNames = nameParts[nameParts.length - 1];

      if (event.target.value === "") {
        this.showDetailedName = false;
      } else if (nameParts.length > 2) {
        this.showDetailedName = true;
      }
  }

  updateFullName() {
    this.fullName = [this.firstNames, this.middleNames, this.lastNames]
      .filter(a => a !== "")
      .join(" ");

      if (this.fullName === "") {
        this.showDetailedName = false;
        this.$refs.memberType.focus();
      }
  }

  showMembership() {
    this.showMembershipType = true;

      const memberType = this.$refs.memberType as HTMLElement;

      setTimeout(() => memberType.focus(), 200);
      setTimeout(
        () => memberType.classList.add("uk-form-danger"),
        200
      );
      setTimeout(
        () => memberType.classList.remove("uk-form-danger"),
        2000
      );
  }

  submitRegistration() {
    fetch('/portal/api/register/', {
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.csrf_token
      },
      body: JSON.stringify(this.$data)
    })
  }

}
</script>

<template lang="pug">
div
  form.uk-form-horizontal.uk-align-center(class='uk-width-1-2@s' method='POST')
    .uk-form-row.uk-margin-bottom
      #div_id_fullName
        label.uk-form-label(for='id_givenName') Full Name *
        .uk-form-controls
          input.uk-input(ref='name' maxlength='255' name='fullname' required='' type='text' @input='checkName' autocomplete='name' autofocus='' v-model='fullName' placeholder='Jonathan Smith')
      #div_id_givenName.uk-margin-large-left.uk-margin-top(v-show='showDetailedName')
        label.uk-form-label(for='id_givenName') Given Names *
        .uk-form-controls.uk-form-controls-text
          input#id_givenName.uk-input(maxlength='255' name='givenName' v-model='firstNames' required='' type='text' @input='updateFullName')
      #div_id_middleName.uk-margin-large-left(v-show='showDetailedName')
        label.uk-form-label(for='id_middleName') Middle Names
        .uk-form-controls.uk-form-controls-text
          input#id_middleName.uk-input(maxlength='255' name='middleNames' type='text' v-model='middleNames' @input='updateFullName')
      #div_id_familyName.uk-margin-large-left(v-show='showDetailedName')
        label.uk-form-label(for='id_familyName') Family Names *
        .uk-form-controls.uk-form-controls-text
          input#id_familyName.uk-input(maxlength='255' name='familyName' v-model='lastNames' required='' type='text' @input='updateFullName' ref='familynames')
    .uk-form-row
      #div_id_email
        label.uk-form-label(for='id_email') Email *
        .uk-form-controls.uk-form-controls-text
          input#id_email.uk-input(maxlength='254' name='email' required='' type='email' autocomplete='email' list='email-suggestions' placeholder='j.smith@example.com' v-model='email' @focus='showEmailSuggestions = true' @blur='showEmailSuggestions = false')
          datalist#email-suggestions(style='display: block;' v-show='showEmailSuggestions')
            option(v-for='suggestion in emailSuggestions' v-bind:key='suggestion' v-bind:value='suggestion')
        .uk-form-label(class='uk-hidden@m')
          br
      #div_id_birthday
        label.uk-form-label(for='id_birthday') Birthday *
        .uk-form-controls-text(class='uk-hidden@m')
          p
        .uk-form-controls.uk-form-controls-text
          input#id_birthday.uk-input(name='birthday' required='' type='date' v-model='birthDate')
        .uk-form-controls.uk-form-controls-text(class='uk-visible@m')
          p
        .uk-form-label(class='uk-hidden@m')
          br
      //
        <div class="uk-margin">
        <label class="uk-form-label" for="id_existing"></label>
        <div class="uk-form-controls uk-form-controls-text">
        <input
        class="uk-checkbox"
        id="id_existing"
        name="accountExists"
        required
        type="checkbox"
        v-model="accountExists"
        />
        I have an existing alumni e-mail
        </div>
        </div>
      #div_id_existingEmail(v-show='accountExists')
        label.uk-form-label(for='id_email') Existing e-mail
        .uk-form-controls-text(class='uk-hidden@m')
          p
            | Existing
            em @jacobs-alumni.de
            |  email address (if you have one)
        .uk-form-controls.uk-form-controls-text
          input#id_existingEmail.uk-input(maxlength='254' name='existingEmail' type='email' list='alumnimails' v-model='alumniemail')
          datalist#alumnimails(style='display: block;')
            option(v-for='suggestion in alumniEmailSuggestions' :key='suggestion' :value='suggestion')
      #div_id_resetExistingEmailPassword(v-show='accountExists')
        .uk-form-controls-text(class='uk-hidden@m')
          p
        .uk-form-controls.uk-form-controls-text
          input#id_resetExistingEmailPassword.uk-checkbox(name='resetExistingEmailPassword' type='checkbox')
          | Reset password to existing email address
        .uk-form-controls.uk-form-controls-text(class='uk-visible@m')
          p
        .uk-form-label(class='uk-hidden@m')
          br
    .uk-form-row
      div(v-show='showMembershipType')
        label.uk-form-label(for='id_type') I am *
        .uk-form-controls.uk-form-controls-text
          select#id_type.uk-select(name='memberType' ref='memberType' v-model='memberType')
            option(value='al') Alum / Alumna
            option(value='fs') Faculty or Staff
            option(value='fr') Friend of the association
      div
        label.uk-form-label(for='id_tier') Yearly Contribution *
        .uk-form-controls.uk-form-controls-text
          select#id_tier.uk-select(name='memberTier' v-model="memberTier")
            option(v-for='(description, value) in tierChoices' :key='value' :value='value') {{ description }}
    .uk-form-row
      #div_id_tos.uk-margin-bottom.uk-margin-top
        label.uk-form-label(for='id_tos') Terms and Conditions *
        .uk-form-controls.uk-form-controls-text
          input#id_tos.uk-checkbox(name='tos' required='' type='checkbox' v-model='tos')
          |                 I confirm that I have read and agree to the 
          a(href='https://jacobs-alumni.de/privacy/' target='_blank') Terms and Conditions
          | , the 
          a(href='https://jacobs-alumni.de/charter' target='_blank') Charter
          | , and the 
          a(href='https://www.jacobs-alumni.de/by-laws' target='_blank') Contributions By-Laws
          | .
    
    input#input_id_other_type.uk-button.uk-width-1-1.uk-button-default(class='uk-width-1-2@m' value='I Am Not Alumnus' @click='showMembership' v-show='!showMembershipType')
    input#input_id_submit.uk-button.uk-button-primary(@click.prevent="submitRegistration" :class="{'uk-width-1-1': showMembershipType, 'uk-width-1-1 uk-width-1-2@m': !showMembershipType}" type='submit' :value="'Sign Up As ' + signUpText")

    input(type='hidden' name='csrfmiddlewaretoken' :value='csrf_token')
</template>
