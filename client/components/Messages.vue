<template>
  <div class="messages stackable ui stories container grid">
    <lgheader title="Messages"></lgheader>

    <div class="four wide column">
      <h3>Filters</h3>
      <div class="ui form">
        <lginput :value.sync="userQuery" id="query" type="text" label="User Search"></lginput>
      </div>
    </div>
    <div class="twelve wide column">
      <h3>Groups</h3>
      <div class="message-table-container">
        <table class="ui red celled fixed table">
          <thead>
            <tr>
              <th>Current Clue</th>
              <th>User</th>
              <th>Last Message</th>
              <th>Date Started</th>
              <th>Date Completed</th>
              <th>Controls</th>
            </tr>
          </thead>
          <tr v-for="group in sortedGroups">
            <td>
              {{group.clue_uid}}
            </td>
            <td>
              <div v-for="key in group.user_keys">{{key}}</div>
            </td>
            <td>
              {{group.messaged_at | formatDate}}
            </td>
            <td>
              {{group.created_at | formatDate}}
            </td>
            <td>
              {{group.completed_at | formatDate}}
            </td>
            <td>
              <router-link class="ui button" :to="{ name: 'Group', 'params': {uid: group.uid}}">Transcript</router-link>
            </td>
          </tr>
        </table>
      </div>

      <h3>Users</h3>
      <div class="message-table-container">
        <table class="ui blue celled fixed table">
          <thead>
            <tr>
              <th>User</th>
              <th>Group ID</th>
              <th>Last Message</th>
              <th>Date Started</th>
              <th>Controls</th>
            </tr>
          </thead>
          <tr v-for="user in sortedUsers">
            <td>
              {{user.user_uid}}
            </td>
            <td>
              {{user.group_uid}}
            </td>
            <td>
              {{user.messaged_at | formatDate}}
            </td>
            <td>
              {{user.registration_date | formatDate}}
            </td>
            <td>
              <router-link class="ui button" :to="{ name: 'User', 'params': {uid: user.user_uid}}">Transcript</router-link>
            </td>
          </tr>
        </table>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: 'Messages',
  data () {
    return {
      users: [],
      userQuery: "",
      groups: []
    }
  },
  computed: {
    sortedGroups: function () {
      function createCompare(b, a) {
        return new Date(a.created_at) - new Date(b.created_at); 
      }
      function messagedCompare(b, a) {
        return new Date(a.messaged_at) - new Date(b.messaged_at);
      }
      return this.filteredGroupsBySearch.sort(createCompare).sort(messagedCompare)
    },
    sortedUsers: function () {
      function createCompare(b, a) {
        return new Date(a.created_at) - new Date(b.created_at); 
      }
      function messagedCompare(b, a) {
        return new Date(a.messaged_at) - new Date(b.messaged_at);
      }
      return this.filteredUsersBySearch.sort(createCompare).sort(messagedCompare)
    },
    filteredUsersBySearch: function () {
      return this.users.filter((user) => (
         user.user_uid.toLowerCase().indexOf(this.userQuery.toLowerCase()) !== -1
        )
      )
    },
    filteredGroupsBySearch: function () {
      return this.groups.filter((group) => (
         group.user_keys[0].toLowerCase().indexOf(this.userQuery.toLowerCase()) !== -1
        )
      )
    },
  },
  mounted() {
    axios.get('/api/groups/?paged=false')
      .then(response => {
        this.groups = response.data.data;
      }),
      axios.get('/api/users/?paged=false')
      .then(response => {
        this.users = response.data.data;
      })
  }
}
</script>
<style>
.message-table-container {
  max-height: 500px;
  overflow-y: scroll;
}
</style>
