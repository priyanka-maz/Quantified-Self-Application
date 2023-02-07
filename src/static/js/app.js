const api_host = 'http://localhost:8080';

const Tracker = Vue.component('tracker', {
    template: `
    <div>
        <h3 class="h3">Trackers</h3>
            <h6 class="h6">User: {{user.email}}</h6>
            <button class="btn btn-success" v-if="form_hidden" v-on:click="form_hidden = !form_hidden">Add Tracker</button>
            <button class="btn btn-danger" v-if="!form_hidden" v-on:click="form_hidden = !form_hidden">Cancel</button>
            <p></p>
            <div v-if="!form_hidden">
                <p>
                    <label for="tracker_name">Name</label> <input id="tracker_name" required v-model="tracker_name" value="">
                </p>

                <p>
                    <label for="tracker_desc">Description</label> <input id="tracker_desc" required v-model="tracker_desc" value="">
                </p>
                <p>
                    <label>Type</label>
                    <div style="margin-left:6%" class="form-check">
                        <input class="form-check-input" type="radio" id="tracker_type" required v-model="tracker_type" value="mcq">
                        <label class="form-check-label" for="tracker_type">Multiple Choice</label><br>
                        <input class="form-check-input" type="radio" id="tracker_type" required v-model="tracker_type" value="num">
                        <label class="form-check-label" for="tracker_type">Numerical</label><br>
                        <input class="form-check-input" type="radio" id="tracker_type" required v-model="tracker_type" value="bool">
                        <label class="form-check-label" for="tracker_type">Boolean</label><br>
                        <input class="form-check-input" type="radio" id="tracker_type" required v-model="tracker_type" value="time">
                        <label class="form-check-label" for="tracker_type">Time Duration</label><br>
                    </div>
                </p>
                <p>
                    <label for="tracker_mcq">Values</label> <input id="tracker_mcq" v-model="tracker_mcq" value="">
                    <h8 class="h8">Add options for Multiple Choice</h8>
                </p>
                <p></p>
                <p><input class="btn btn-success" id="submit" type="submit" v-on:click="new_tracker" value="Submit"></p>
            </div>
            <div v-if="form_hidden">
                <div class="row mb-2 bg-primary text-white rounded">
                    <div class="col-2">
                            <span>Tracker</span>
                    </div>
                    <div class="col-2">
                            <span>Last Reviewed</span>
                    </div>
                    <div class="col-2">
                            <span>Edit</span>
                    </div>
                    <div class="col-2">
                            <span>Delete</span>
                    </div>
                </div>

                <div class="row mb-4 bg-light" v-for="(tracker, index) in trackers">
                    <div class="col-2">
                        <router-link class="btn btn-outline-primary" v-bind:to="'/log?tracker_id=' + tracker.id">{{tracker.name}}</router-link>
                    </div>
                    <div class="col-2">
                        <span>{{tracker.timestamp}}</span>
                    </div>
                    <div class="col-2">
                        <button class="btn btn-warning" v-if="update_hidden" v-on:click="update_hidden = !update_hidden; selected = index">Edit</button>
                    </div>

                    <div class="col-2">
                        <button type="button" class="btn btn-danger" v-on:click="del_tracker(tracker.id)">Delete</button>
                    </div>

                    <div v-if="!update_hidden && selected == index">
                    	<p></p>
                        <p>
                            <label for="tracker_name">Name</label> <input id="tracker_name" v-model="tracker_name" value="">
                        </p>
                        <p>
                            <label for="tracker_desc">Description</label> <input id="tracker_desc" v-model="tracker_desc" value="">
                        </p>
                        <p></p>
                        <p>
                            <input class="btn btn-warning" id="submit" type="submit" v-on:click="edit_tracker(tracker.id)" value="Submit">
                            <button class="btn btn-danger" v-if="!update_hidden" v-on:click="update_hidden = !update_hidden">Cancel</button>
                        </p>
            	    </div>
                </div>
            </div>
    </div>`,
    data: function () {
        return {
            form_hidden: true,
            update_hidden: true,
            trackers: null,
            tracker_name: null,
            tracker_desc: null,
            tracker_type: null,
            tracker_mcq:  null,
            selected: 	  null,
            user: 	  null,
        }
    },
    methods: {
        new_tracker: function () {
            fetch(api_host + '/api/tracker', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    'name': this.tracker_name,
                    'desc': this.tracker_desc,
                    'type': this.tracker_type,
                    'mcq':  this.tracker_mcq,
                }),
            }).then(response => {
                if (!response.ok) {
                    alert('Failed to create tracker.');
                    this.$router.go();
                } else {
                    return response.json();
                }
            }).then(data => {
                this.trackers.push(data);
                this.tracker_name = null;
                this.tracker_desc = null;
                this.tracker_type = null;
                this.tracker_mcq = null;
                this.form_hidden = true;
                this.$router.go();
            }).catch((error) => {
                console.error('Error:', error);
            });
        },
        del_tracker: function (tracker_id) {
            fetch(api_host + '/api/tracker?tracker_id=' + tracker_id, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
            }).then(response => {
                if (!response.ok) {
                    alert('Failed to delete tracker.');
                    this.$router.go();
                } else {
                    return response.json();
                }
            }).then(data => {
                this.trackers.splice(this.trackers.indexOf(data), 1);
                window.location.reload(true);
            }).catch((error) => {
                console.error('Error:', error);
            });
        },
        edit_tracker: function (tracker_id) {
            fetch(api_host + '/api/tracker?tracker_id=' + tracker_id, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    'name': this.tracker_name,
                    'desc': this.tracker_desc,
                }),
            }).then(response => {
                if (!response.ok) {
                    alert('Failed to edit tracker.');
                    this.$router.go();
                } else {
                    return response.json();
                }
            }).then(data => {
            	this.tracker_name = null;
                this.tracker_desc = null;
                this.update_hidden = true;
                window.location.reload(true);
            }).catch((error) => {
                console.error('Error:', error);
            });
           }
    },
    created: function () {
        fetch(api_host + '/api/tracker', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        }).then(response => {
            if (!response.ok) {
                alert('Failed to fetch trackers.');
            } else {
                return response.json();
            }
        }).then(data => {
            this.trackers = data;
        }).catch((error) => {
            console.error('Error:', error);
        });

        fetch(api_host + '/api/user', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        }).then(response => {
            if (!response.ok) {
                alert('Failed to fetch user.');
            } else {
                return response.json();
            }
        }).then(data => {
            this.user = data;
            console.log(this.user.email);
        }).catch((error) => {
            console.error('Error:', error);
        });

    }
});

const Log = Vue.component('log', {
    template: `
    <div>
        <h3>{{tracker.name}} Tracker Logs</h3>
            <h6>About: {{tracker.desc}}</h6>
            <img v-bind:src="'data:image/png;base64,'+tracker.bstr" alt="Chart" />
            <button class="btn btn-success" v-if="form_hidden" v-on:click="form_hidden = !form_hidden">Add Log</button>
            <button class="btn btn-danger" v-if="!form_hidden" v-on:click="form_hidden = !form_hidden">Cancel</button>
            <p></p>
            <div v-if="!form_hidden">
                <p v-if="tracker.type === 'num'">
                    <label for="log_value">Value</label><input type="number" id="log_value" required v-model="log_value" value=""/>
                </p>
                <p v-if="tracker.type === 'bool'">Value
		            <br>
                    <input  type="radio" id="log_value" required v-model="log_value" value="True">
                    <label  for="log_value">True</label><br>
                    <input  type="radio" id="log_value" required v-model="log_value" value="False">
                    <label  for="log_value">False</label><br>
                </p>
                <p v-if="tracker.type === 'time'">
                    <label for="log_value">Value</label><input type="time" id="log_value" required v-model="log_value" value=""/>
                </p>
                <p v-if="tracker.type === 'mcq'">
    		    Options:
    		    <ul><li v-for="op in tracker.mcq.split(',')">{{op}}</li></ul>
		    <label for="log_value">Value</label> <input id="log_value" required v-model="log_value" value="">
		    </p>
                <p>
                    <label for="log_note">Note</label> <input id="log_note" required v-model="log_note" value="">
                </p>

                <p></p>
                <p><input class="btn btn-success" id="submit" type="submit" v-on:click="new_log" value="Submit"></p>
            </div>
            <div v-if="form_hidden">
            	<div class="row mb-2 bg-primary text-white rounded">
                    <div class="col-2">
                            <span>Log</span>
                    </div>
                    <div class="col-2">
                            <span>Note</span>
                    </div>
                    <div class="col-2">
                            <span>Last Reviewed</span>
                    </div>
                    <div class="col-2">
                            <span>Edit</span>
                    </div>
                    <div class="col-2">
                            <span>Delete</span>
                    </div>
                </div>
                <div class="row mb-4 bg-light" v-for="(log, index) in logs">
                    <div class="col-2">
                        <button class="btn btn-outline-primary">{{log.value}}</button>
                    </div>
                    <div class="col-2">
                        <span>{{log.note}}</span>
                    </div>
                    <div class="col-2">
                        <span  v-if="log.timestamp"> {{log.timestamp}} </span>
                        <span v-if="!log.timestamp || log.timestamp === ''"> Not reviewed yet. </span>
                    </div>
                    <div class="col-2">
                        <button class="btn btn-warning" v-if="update_hidden" v-on:click="update_hidden = !update_hidden; selected = index">Edit</button>
                    </div>

                    <div class="col-2">
                        <button type="button" class="btn btn-danger" v-on:click="del_log(log.id)">Delete</button>
                    </div>

                    <div v-if="!update_hidden && selected == index">
                    	<p></p>
                        <p v-if="tracker.type === 'num'">
                            <label for="log_value">Value</label><input type="number" id="log_value" v-model="log_value" value=""/>
                        </p>
                        <p v-if="tracker.type === 'bool'">Value
			    <br>
		            <input  type="radio" id="log_value" v-model="log_value" value="True">
		            <label  for="log_value">True</label><br>
		            <input  type="radio" id="log_value" v-model="log_value" value="False">
		            <label  for="log_value">False</label><br>
                        </p>

                        <p v-if="tracker.type === 'time'">
                            <label for="log_value">Value</label><input type="time" id="log_value" v-model="log_value" value=""/>
                        </p>
                        <p v-if="tracker.type === 'mcq'">
            	    	    Options:
                            <ul><li v-for="op in tracker.mcq.split(',')">{{op}}</li></ul>
                            <label for="log_value">Value</label> <input id="log_value" v-model="log_value" value="">
			</p>
                        <p>
                            <label for="log_note">Note</label> <input id="log_note" v-model="log_note" value="">
                        </p>
                	<p>
                    	    <label for="log_timestamp">Timestamp</label> <input type="datetime-local" id="log_timestamp" v-model="log_timestamp" value="">
                	</p>
                        <p></p>
                        <p>
                            <input class="btn btn-warning" id="submit" type="submit" v-on:click="edit_log(log.id)" value="Submit">
                            <button class="btn btn-danger" v-if="!update_hidden" v-on:click="update_hidden = !update_hidden">Cancel</button>
                        </p>
            	    </div>
                </div>
            </div>
    </div>`,

    data: function () {
        return {
            form_hidden: true,
            update_hidden: true,
            logs: null,
            log_note: null,
            log_value: null,
            log_timestamp: null,
            selected: 	  null,
            tracker: null,

        }
    },
    methods: {
        new_log: function () {
            fetch(api_host + '/api/log', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    'tracker_id': this.$route.query.tracker_id,
                    'note': this.log_note,
                    'value': this.log_value,
                    'timestamp': (new Date()).toGMTString(),
                }),
            }).then(response => {
                if (!response.ok) {
                    alert('Failed to create log.');
                    this.$router.go();
                } else {
                    return response.json();
                }
            }).then(data => {
                this.logs.push(data);
                this.log_note = null;
                this.log_value = null;
                this.form_hidden = true;
                this.$router.go();

            }).catch((error) => {
                console.error('Error:', error);
            });

            fetch(api_host + '/api/tracker?tracker_id=' + this.$route.query.tracker_id, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            }).then(response => {
                if (!response.ok) {
                    alert('Failed to fetch tracker.');
                } else {
                    return response.json();
                }
            }).then(data => {
                this.tracker = data;
            }).catch((error) => {
                console.error('Error:', error);
            });

        },

        del_log: function (log_id) {
            fetch(api_host + '/api/log?log_id=' + log_id, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
            }).then(response => {
                if (!response.ok) {
                    alert('Failed to delete log.');
                    this.$router.go();
                } else {
                    return response.json();
                }
            }).then(data => {
                this.logs.splice(this.logs.indexOf(data), 1);
                window.location.reload(true);
            }).catch((error) => {
                console.error('Error:', error);
            });

            fetch(api_host + '/api/tracker?tracker_id=' + this.$route.query.tracker_id, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            }).then(response => {
                if (!response.ok) {
                    alert('Failed to fetch tracker.');
                } else {
                    return response.json();
                }
            }).then(data => {
                this.tracker = data;
            }).catch((error) => {
                console.error('Error:', error);
            });

        },
        edit_log: function (log_id) {
            fetch(api_host + '/api/log?log_id=' + log_id, {
                method: 'PUT',
                headers: {

                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    'note': this.log_note,
                    'value': this.log_value,
                    'timestamp': new Date(this.log_timestamp).toGMTString(),
                }),
            }).then(response => {
                if (!response.ok) {
                    alert('Failed to edit log.');
                    this.$router.go();
                } else {
                    return response.json();
                }
            }).then(data => {
            	this.log_note = null;
                this.log_value = null;
                this.update_hidden = true;
                window.location.reload(true); //reload, not from cache for edits //or use this.$router.go();
            }).catch((error) => {
                console.error('Error:', error);
            });

            fetch(api_host + '/api/tracker?tracker_id=' + this.$route.query.tracker_id, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            }).then(response => {
                if (!response.ok) {
                    alert('Failed to fetch tracker.');
                } else {
                    return response.json();
                }
            }).then(data => {
                this.tracker = data;
            }).catch((error) => {
                console.error('Error:', error);
            });

           }
    },
    created: function () {
        fetch(api_host + '/api/log?tracker_id=' + this.$route.query.tracker_id, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        }).then(response => {
            if (!response.ok) {
                alert('Failed to fetch logs.');
            } else {
                return response.json();
            }
        }).then(data => {
            this.logs = data;
        }).catch((error) => {
            console.error('Error:', error);
        });

        fetch(api_host + '/api/tracker?tracker_id=' + this.$route.query.tracker_id, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        }).then(response => {
            if (!response.ok) {
                alert('Failed to fetch tracker.');
            } else {
                return response.json();
            }
        }).then(data => {
            this.tracker = data;
	    //this.tracker_bstr = this.tracker.bstr.substring(2);
	    //this.tracker_bstr = this.tracker_bstr.replace("'", "=");

        }).catch((error) => {
            console.error('Error:', error);
        });

    },

});

const Account = Vue.component('account', {
    template: `
    <div>
        <div v-if="form_hidden">
            <h3>Account</h3>
                <button type="button" class="btn btn-secondary" v-on:click="tracker_export">Export trackers as CSV</button>
                <button type="button" class="btn btn-secondary" v-on:click="tracker_import">Import trackers as CSV</button>
                <p></p>
                <button type="button" class="btn btn-info" v-on:click="gen_report_html">Generate HTML Report</button>
                <button type="button" class="btn btn-info" v-on:click="gen_report_pdf">Generate PDF Report</button>
                <p></p>
                <button type="button" class="btn btn-danger" v-on:click="del_user">Delete Account</button>
                <p></p>
        </div>
        <div v-if="!form_hidden">
            <form action="/import" method="post" enctype="multipart/form-data">
              Select file to upload:
              <input type="file" name="file" id="file">
              <input type="submit" value="Upload File" name="submit">
            </form>
        </div>
    </div>`,
    data: function () {
        return {
            form_hidden: true,
        }
    },
    methods: {
        tracker_export: function () {
            window.open(api_host + '/export', '_blank').focus();
        },
        tracker_import: function () {
            this.form_hidden = false;
        },
        gen_report_html: function () {
            window.open(api_host + '/report', '_blank').focus();
        },
        gen_report_pdf: function () {
            fetch(api_host + '/report?format=pdf', {
                method: 'GET',
            }).then(response => {
                if (!response.ok) {
                    alert('Failed to get report.');
                }
                return response.blob();
            }).then(blob => {
                const file_url = window.URL.createObjectURL(blob);
                const file_link = document.createElement('a');
                file_link.href = file_url;
                file_link.download = "user_report.pdf";
                document.body.appendChild(file_link);
                file_link.click();
                file_link.remove();
            }).catch((error) => {
                console.error('Error:', error);
            });
        },
        del_user: function () {
            fetch(api_host + '/api/user', {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
            }).then(response => {
                if (!response.ok) {
                    alert('Failed to delete user.');
                }
                return response.json();
            }).then(data => {
                this.$router.go({path: '/'});
            }).catch((error) => {
                console.error('Error:', error);
            });
        },
    },
    created: function () {
    },
});

const Logout = Vue.component('logout', {
    created: function () {
        window.location.replace(api_host + '/no_cache');
    }
});

const NotFound = {template: '<h1>Not Found</h1><p>The requested URL was not found on the server.</p>'}

const router = new VueRouter({
    routes: [{
        path: '/',
        component: Tracker
    }, {
        path: '/log',
        component: Log
    }, {
        path: '/account',
        component: Account
    }, {
        path: '/logout',
        component: Logout
    }]
})


var app = new Vue({
    el: '#app',
    delimiters: ['${', '}'],
    router: router,
})
