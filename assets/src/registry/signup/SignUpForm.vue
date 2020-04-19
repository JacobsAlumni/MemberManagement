<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';

import getCookie from "../../base/utils/cookie";
import VueValidatable from "../../base/utils/validate";
import {MemberType, MemberTypeDescriptions, MemberTier, getAllowedTiers, MemberTierShortTitles, MemberTierDescriptions} from "../../base/utils/membership";

// autocomplete on the most common providers
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

// the default birthday
const birthDayDefault = new Date();
birthDayDefault.setFullYear(birthDayDefault.getFullYear() - 24);
const birthDayDefaultString = `${birthDayDefault.getFullYear()}-${(birthDayDefault.getMonth() + 1)
        .toString()
        .padStart(2, "0")}-${birthDayDefault
        .getDate()
        .toString()
        .padStart(2, "0")}`;

@Component
export default class SignupForm extends VueValidatable {
  declare $refs: {
    memberType: HTMLInputElement;
    registerForm: HTMLFormElement;
  };

  // form validation
  get formInstance() {
    return this.$refs.registerForm;
  }
  readonly formKeys = ['givenNames', 'middleNames', 'familyNames', 'birthday', 'email', 'memberType', 'memberTier', 'tos'];
  readonly validateEndpoint = "/portal/register/validate/";
  readonly submitEndpoint = null;

  // TODO: Split the name handling into a seperate component

  /**
   * given a partial list of names, returns the fullName
   */
  private static joinFullName(givenNames: string, middleNames: string, familyNames: string): string {
    return [givenNames, middleNames, familyNames]
      .filter(a => a !== "")
      .join(" ");
  }

  /** given a full name, split it into indivodual components */
  private static splitFullName(fullName: string): [string, string, string] {
    // split names by spaces into first, middle, last
    const [first, ...middle] = fullName.trim().split(/\s+/g);
    const last = middle.pop();

    // return each component seperatly
    return [
      first,
      middle.join(" "),
      last || ""
    ];
  }

  givenNames = this.initialValidationResult.values['givenNames'] || "";
  middleNames = this.initialValidationResult.values['middleNames'] || "";
  familyNames = this.initialValidationResult.values['familyNames'] || "";
  fullName = SignupForm.joinFullName(this.givenNames, this.middleNames, this.familyNames);
  showDetailedName = this.middleNames !== "";

  handleFullNameChange(event: KeyboardEvent & {target: HTMLInputElement}) {
      [this.givenNames, this.middleNames, this.familyNames] = SignupForm.splitFullName(event.target.value || "");
      this.showDetailedName = this.middleNames !== "";

      // and also validate
      this.validateFormDebounced()
  }

  handlePartNameChange() {
    this.fullName = SignupForm.joinFullName(this.givenNames, this.middleNames, this.familyNames);
    this.showDetailedName = this.middleNames !== "";

    if (!this.showDetailedName) {
      this.$refs.memberType.focus();
    }

    // and run validation
    this.validateFormDebounced();
  }
  
  // email
  email = this.initialValidationResult.values["email"] || "";
  showEmailSuggestions = false;

  get emailSuggestions(): string[] {
    const emailParts = this.$data.email.split("@");
    if (!this.email || !emailParts) {
      return [];
    }

    return emailProviders.map(
      providerDomain => emailParts[0] + "@" + providerDomain
    );
  }

  // birthday
  birthday = this.initialValidationResult.values["birthday"] || birthDayDefaultString;

  // membertype
  memberType: MemberType = this.initialValidationResult.values["memberType"] as MemberType || MemberType.Alumnus;
  showMembershipType = this.memberType !== MemberType.Alumnus;
  showMembership() {
    this.showMembershipType = true;

      const memberType = this.$refs.memberType;

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

  // member tier
  memberTier: MemberTier = this.initialValidationResult.values["memberTier"] as MemberTier || MemberTier.Contributor;
    get tierChoices(): Record<string, string> {
    return getAllowedTiers(this.memberType).reduce<Record<string, string>>((acc, v) => {
      acc[v] = MemberTierShortTitles[v];
      return acc;
    }, {});
  };

  // tos, these always need to be re-checked
  tos = false;
  get signUpText(): string {
    return MemberTypeDescriptions[this.memberType];
  }

  // TODO: This is currently not supported
  accountExists = false;
  alumniemail = "";
  get alumniEmailSuggestions(): string[] {
    const emailParts = this.$data.alumniemail.split("@");
    if (!this.alumniemail || !emailParts) {
      return [];
    }

    return [emailParts[0] + "@jacobs-alumni.de"];
  }

  // csrf token
  csrf_token = getCookie('csrftoken')!;
}
</script>

<template lang="pug">
div
  form.uk-form-horizontal(method='POST' ref='registerForm')
    // csrf
    input(type='hidden' name='csrfmiddlewaretoken' :value='csrf_token')

    // form errors
    .uk-alert-danger.uk-alert(v-for="error in validateResult.errors.__all__")
      p {{ error.message }}

    // name
    .uk-form-row
      #div_id_fullName
        label.uk-form-label(for='id_givenName') Full Name *
        .uk-form-controls
          input.uk-input.uk-margin-bottom(ref='name' maxlength='255' name='fullname' required='' type='text' @input='handleFullNameChange' autocomplete='name' autofocus='' v-model='fullName' placeholder='Jonathan Smith')
          .div(v-show='!showDetailedName')
            .uk-alert-danger.uk-alert(v-for="error in validateResult.errors.givenNames")
                p Given Names: {{ error.message }}
            .uk-alert-danger.uk-alert(v-for="error in validateResult.errors.middleNames")
                p Middle Names: {{ error.message }}
            .uk-alert-danger.uk-alert(v-for="error in validateResult.errors.familyNames")
                p Family Names: {{ error.message }}

      #div_id_givenNames.uk-margin-large-left.uk-margin-top(v-show='showDetailedName')
        label.uk-form-label(for='id_givenNames') Given Names *
        .uk-form-controls.uk-form-controls-text
          input#id_givenNames.uk-input(maxlength='255' name='givenNames' v-model='givenNames' required='' type='text' @input='handlePartNameChange')
          .uk-alert-danger.uk-alert(v-for="error in validateResult.errors.givenNames")
            p {{ error.message }}
      
      #div_id_middleNames.uk-margin-large-left(v-show='showDetailedName')
        label.uk-form-label(for='id_middleNames') Middle Names
        .uk-form-controls.uk-form-controls-text
          input#id_middleNames.uk-input(maxlength='255' name='middleNames' type='text' v-model='middleNames' @input='handlePartNameChange')
          .uk-alert-danger.uk-alert(v-for="error in validateResult.errors.middleNames")
            p {{ error.message }}
      
      #div_id_familyNames.uk-margin-large-left(v-show='showDetailedName')
        label.uk-form-label(for='id_familyNames') Family Names *
        .uk-form-controls.uk-form-controls-text
          input#id_familyNames.uk-input(maxlength='255' name='familyNames' v-model='familyNames' required='' type='text' @input='handlePartNameChange' ref='familynames')
          .uk-alert-danger.uk-alert(v-for="error in validateResult.errors.familyNames")
            p {{ error.message }}
    
    // email
    .uk-form-row
      #div_id_email
        label.uk-form-label(for='id_email') Email *
        .uk-form-controls.uk-form-controls-text
          input#id_email.uk-input(maxlength='254' name='email' required='' type='email' autocomplete='email' list='email-suggestions' placeholder='j.smith@example.com' v-model='email' @change='validateFormDebounced' @focus='showEmailSuggestions = true' @blur='showEmailSuggestions = false')
          datalist#email-suggestions(v-show='showEmailSuggestions')
            option(v-for='suggestion in emailSuggestions' v-bind:key='suggestion' v-bind:value='suggestion')
          .uk-alert-danger.uk-alert(v-for="error in validateResult.errors.email")
            p {{ error.message }}
      
    // birthday
    .uk-form-row
      #div_id_birthday
        label.uk-form-label(for='id_birthday') Birthday *
        .uk-form-controls.uk-form-controls-text
          input#id_birthday.uk-input(name='birthday' required='' type='date' v-model='birthday' @input='validateFormDebounced')
        .uk-alert-danger.uk-alert(v-for="error in validateResult.errors.birthday")
          p {{ error.message }}
    
    // membership type
    .uk-form-row(v-show='showMembershipType')
      #div_id_type
        label.uk-form-label(for='id_type') I am *
        .uk-form-controls.uk-form-controls-text
          select#id_type.uk-select(name='memberType' ref='memberType' v-model='memberType')
            option(value='re') Alum / Alumna
            option(value='fa') Faculty or Staff
            option(value='fr') Friend of the association
        .uk-alert-danger.uk-alert(v-for="error in validateResult.errors.memberType")
          p {{ error.message }}
    input(v-show='!showMembershipType' type='hidden' name='memberType' :value='memberType')
    
    // membership tier
    .uk-form-row
      #div_id_tier
        label.uk-form-label(for='id_tier') Yearly Contribution *
        .uk-form-controls.uk-form-controls-text
          select#id_tier.uk-select(name='memberTier' v-model="memberTier")
            option(v-for='(description, value) in tierChoices' :key='value' :value='value') {{ description }}
        .uk-alert-danger.uk-alert(v-for="error in validateResult.errors.memberTier")
          p {{ error.message }}
    
    // terms an conditions
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
          .uk-alert-danger.uk-alert(v-for="error in validateResult.errors.tos")
            p {{ error.message }}

    // submit buttons
    input#input_id_other_type.uk-button.uk-width-1-1.uk-button-default(class='uk-width-1-2@m' value='I Am Not Alumnus' @click='showMembership' v-show='!showMembershipType')
    input#input_id_submit.uk-button.uk-button-primary(@click.prevent="submitForm" :class="{'uk-width-1-1': showMembershipType, 'uk-width-1-1 uk-width-1-2@m': !showMembershipType}" type='submit' :value="'Sign Up As ' + signUpText")

    // TODO: Existing email
      
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
          input#id_existingEmail.uk-input(maxlength='254' name='existingEmail' type='email' list='alumnimails' v-model='alumniemail' )
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

</template>
