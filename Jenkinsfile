def get_test_env() {
    if (env.JOB_NAME.toLowerCase().contains('apiqa')) {
        return 'regression'
    } else if (env.JOB_NAME.toLowerCase().contains('_feature_')) {
        return 'ci'
    }
}

def get_test_type() {
    if (env.JOB_NAME.toLowerCase().contains('regression')) {
        return 'regression'
    } else if (env.JOB_NAME.toLowerCase().contains('ci')) {
        return 'ci'
    }
}

def get_service() {
    if (env.JOB_NAME.toLowerCase().contains('_jaeger_')) {
        return 'jaeger'
    } else if (env.JOB_NAME.toLowerCase().contains('_bastion_')) {
        return 'bastion'
    } else if (env.JOB_NAME.toLowerCase().contains('_hbp_')) {
        return 'hbp'
    } else if (env.JOB_NAME.toLowerCase().contains('_scrat_')) {
        return 'scrat'
    } else if (env.JOB_NAME.toLowerCase().contains('_bflat_')) {
        return 'bflat'
    }
}

def get_default_host_endpoint(service, test_env) {
    def config = readJSON text: '''{
        "jaeger": {
            "regression": "jaeger-reg-all-instance.apiqa.svc.cluster.local",
            "ci": "FROM_UPSTREAM_JENKINS_JOB"
        },
        "bastion": {
            "regression": "bastion-reg-instance.apiqa.svc.cluster.local",
            "ci": "FROM_UPSTREAM_JENKINS_JOB"
        },
        "hbp": {
            "regression": "hbp-reg-instance.apiqa.svc.cluster.local",
            "ci": "FROM_UPSTREAM_JENKINS_JOB"
        },
        "scrat": {
            "regression": "scrat-reg-all-instance.apiqa.svc.cluster.local",
            "ci": "FROM_UPSTREAM_JENKINS_JOB"
        },
        "bflat": {
            "regression": "bflat-reg.apiqa.svc.cluster.local",
            "ci": "FROM_UPSTREAM_JENKINS_JOB"
        }
    }'''
    return config[service][test_env]
}

def TEST_ENV = get_test_env()
def TEST_TYPE = get_test_type()
def SERVICE = get_service()
def DEFAULT_TEST_CASE_SUITE = SERVICE
def DEFAULT_HOST_ENDPOINT = get_default_host_endpoint(SERVICE, TEST_ENV)

pipeline {

    agent {
        kubernetes {
            label 'Feature_CI_Env'
            yamlFile 'KubernetesPod.yaml'
            defaultContainer 'pytest-ssp-feature'
        }
    }

    environment {   // Local Envs inside of this test pipeline
        ALLURE_RESULT_PATH = './target/allure-result'
    }

    parameters {  // Inter pipeline Envs, Injected by upstream pipeline, or filled out in manual execution from Jenkins UI
        string(name: 'SERVICE_GIT_PR', defaultValue: 'NULL', trim: true, description: 'The PR number of the test target.')
        string(name: 'SERVICE_GIT_COMMIT', defaultValue: 'NULL', trim: true, description: 'The commit hash of the test target.')
        string(name: 'SERVICE_GIT_TAG', defaultValue: 'NULL', trim: true, description: 'The commit tag of the test target.')
        string(name: 'Docker_Image_Version', defaultValue: 'NULL', trim: true, description: 'The version of the docker image which was deployed on the test target.')
        string(name: 'SERVICE_HOST_ENDPOINT', defaultValue: DEFAULT_HOST_ENDPOINT, trim: true, description: 'The host URL of the test service endpoint(w/o port number), can be domain name(e.g jaeger-reg-all.ads-qa.vungle.com) or ELB address(e.g internal-a41c8e6ae67244bbe8def84d1cdabc6d-397113534.us-west-2.elb.amazonaws.com)\nThe default value will be used if leave this field with empty.')
        gitParameter(name: 'TEST_BRANCH', type: 'PT_BRANCH', branchFilter: 'origin/(.*)', defaultValue: 'master', description: 'The branch of the testing repo, master by default.')
        string(name: 'TEST_CASE_SUITE', defaultValue: DEFAULT_TEST_CASE_SUITE, trim: true, description: 'The test case path after the root \"tests/\", the default value will be used if leave this field with empty.\n\nJaeger: \"tests/jaeger\"\nBastion: \"tests/bastion\"\nHBP: \"tests/hbp\"\nScrat: \"tests/scrat\"\nBflat: \"tests/bflat\"')
        choice(name: 'SKIP_INT_CASE', choices: ['NO', 'YES'], description: 'Skip the integration test cases? YES/NO')
    }

    stages {
        stage('Prepare test environment') {
            steps {
                echo 'Preparing test environment...'
                script {
                    echo 'Print the input env data...'
                    echo 'TEST_ENV = ' + TEST_ENV
                    echo 'SKIP_INT_CASE = ' + SKIP_INT_CASE
                    echo 'SERVICE = ' + SERVICE
                    echo 'DEFAULT_TEST_CASE_SUITE = ' + DEFAULT_TEST_CASE_SUITE
                    echo 'TEST_CASE_SUITE = ' + env.TEST_CASE_SUITE
                    echo 'DEFAULT_HOST_ENDPOINT = ' + DEFAULT_HOST_ENDPOINT
                    echo 'SERVICE_HOST_ENDPOINT = ' + env.SERVICE_HOST_ENDPOINT
                    sh('pip3 install google')
                    sh('pip3 install protobuf')

                    def host_key = ''
                    def host_value = ''
                    if (TEST_ENV == 'ci') {
                        if (!env.SERVICE_HOST_ENDPOINT?.trim()) { // if this env variable is empty or null
                            env.SERVICE_HOST_ENDPOINT = DEFAULT_HOST_ENDPOINT
                        }
                    }

                    if (!env.TEST_CASE_SUITE?.trim()) { // if this env variable is empty or null
                        env.TEST_CASE_SUITE = DEFAULT_TEST_CASE_SUITE
                    }

                    if (SERVICE == 'jaeger') {
                        host_key = 'ads_host'
                        if (env.SERVICE_HOST_ENDPOINT?.trim()) {  // if this env variable is not empty or null
                            host_value = 'http://' + env.SERVICE_HOST_ENDPOINT
                        }
                    } else if (SERVICE == 'bastion') {
                        host_key = 'config_host'
                        if (env.SERVICE_HOST_ENDPOINT?.trim()) {  // if this env variable is not empty or null
                            host_value = 'http://' + env.SERVICE_HOST_ENDPOINT
                        }
                    } else if (SERVICE == 'hbp') {
                        host_key = 'hbp_host'
                        if (env.SERVICE_HOST_ENDPOINT?.trim()) {  // if this env variable is not empty or null
                            host_value = 'http://' + env.SERVICE_HOST_ENDPOINT
                        }
                    } else if (SERVICE == 'scrat') {
                        host_key = 'scrat_all_host'
                        if (env.SERVICE_HOST_ENDPOINT?.trim()) {  // if this env variable is not empty or null
                            host_value = 'http://' + env.SERVICE_HOST_ENDPOINT
                        }
                    } else if (SERVICE == 'bflat') {
                        host_key = 'bflat_host'
                        if (env.SERVICE_HOST_ENDPOINT?.trim()) {  // if this env variable is not empty or null
                            if (env.SERVICE_HOST_ENDPOINT.contains('vungle.com')) {
                                host_value = 'http://' + env.SERVICE_HOST_ENDPOINT
                            } else {
                                host_value = 'http://' + env.SERVICE_HOST_ENDPOINT + ':3000'
                            }
                        }
                    }

                    echo 'Updating config... (env=' + TEST_ENV + ', skip_int=' + SKIP_INT_CASE + ', ' + host_key + '=' + host_value + ')'
                    if (env.SERVICE_HOST_ENDPOINT?.trim()) {  // if this env variable is not empty or null
                        sh('python3 update_config.py --env=' + TEST_ENV + ' --skip_int=' + SKIP_INT_CASE + ' --' + host_key + '=' + host_value)
                    } else {
                        sh('python3 update_config.py --env=' + TEST_ENV + ' --skip_int=' + SKIP_INT_CASE)
                    }

                    if (SERVICE == 'jaeger' || SERVICE == 'hbp') {
                        echo "Updating test ads on S3..."
                        if (TEST_TYPE == 'ci') {
                            withCredentials([usernamePassword(credentialsId: 'aws_ansible_qa', passwordVariable: 'AWS_SECRET_ACCESS_KEY', usernameVariable: 'AWS_ACCESS_KEY_ID')]) {
                                sh('py.test -k test_jaeger_prepare_test_ads')
                                sh('sleep 1m')
                            }
                        } else if (TEST_TYPE == 'regression') {
                            withCredentials([usernamePassword(credentialsId: 'role_e2e', passwordVariable: 'AWS_SECRET_ACCESS_KEY', usernameVariable: 'AWS_ACCESS_KEY_ID')]) {
                                sh('py.test -k test_jaeger_prepare_test_ads')
                                sh('sleep 1m')
                            }
                        }
                    }
                }
            }
        }

        stage('Execute Automation Test') {
            steps {
                script {
                    echo 'Running test for ' + SERVICE + ' on ' + TEST_ENV + '...'
                    echo 'TEST_ENV = ' + TEST_ENV
                    echo 'SERVICE = ' + SERVICE
                    echo 'TEST_CASE_SUITE = ' + env.TEST_CASE_SUITE
                    echo 'SERVICE_HOST_ENDPOINT = ' + env.SERVICE_HOST_ENDPOINT

                    sh('rm -rf ' + env.ALLURE_RESULT_PATH)
                    sh('py.test tests/' + env.TEST_CASE_SUITE + ' --alluredir=' + env.ALLURE_RESULT_PATH + ' || true')
                    sh('chmod -R o+xw ' + env.ALLURE_RESULT_PATH)
                }
            }
        }

        stage('Generate allure report') {
            steps {
                script {
                    allure([
                        includeProperties: false,
                        jdk: '',
                        properties: [],
                        reportBuildPolicy: 'ALWAYS',
                        results: [[path: 'target/allure-result']]])
                }
                echo "Test Report: ${env.BUILD_URL}allure/"
            }
        }

        stage('Clear test environment') {
            steps {
                echo 'Clearing test environment...'
                /* script {
                    if (SERVICE == 'jaeger' || SERVICE == 'hbp') {
                        echo 'Rollbacking test ads on S3...'
                        if (TEST_TYPE == 'ci') {
                            withCredentials([usernamePassword(credentialsId: 'aws_ansible_qa', passwordVariable: 'AWS_SECRET_ACCESS_KEY', usernameVariable: 'AWS_ACCESS_KEY_ID')]) {
                                sh('py.test -k test_jaeger_rollback_test_ads')
                            }
                        } else if (TEST_TYPE == 'regression') {
                            withCredentials([usernamePassword(credentialsId: 'role_e2e', passwordVariable: 'AWS_SECRET_ACCESS_KEY', usernameVariable: 'AWS_ACCESS_KEY_ID')]) {
                                sh('py.test -k test_jaeger_rollback_test_ads')
                            }
                        }
                    }
                } */
            }
        }
    }
    post {
        success {
            script {
                if (TEST_TYPE == 'ci') {
                    slackSend (
                        channel: '#ssp-ci',
                        teamDomain: 'vungle',
                        tokenCredentialId: 'jenkins_slack_token',
                        color: '#00FF00',
                        message: "*Test Job:* ${env.JOB_NAME}\n*Build Num:* ${env.BUILD_NUMBER}\n*Test Host:* ${env.SERVICE_HOST_ENDPOINT}\n*Test Result:* :green_light:Passed\n*Test Duration:* ${currentBuild.durationString}\n*Test Report:* ${env.BUILD_URL}allure/\n*Docker Image Version:* ${env.Docker_Image_Version}\n*Service Version:* ${env.SERVICE_GIT_PR}-${env.SERVICE_GIT_COMMIT}-${env.SERVICE_GIT_TAG}\n*Test Case Version:* ${env.GIT_BRANCH}-${env.GIT_COMMIT}\n*Integration Test Skipped:* ${env.SKIP_INT_CASE}"
                    )
                } else if (TEST_TYPE == 'regression') {
                    slackSend (
                        channel: '#jaeger-feed',
                        teamDomain: 'vungle',
                        tokenCredentialId: 'platform_ci_test_slack_token',
                        color: '#00FF00',
                        message: "*Test Job:* ${env.JOB_NAME}\n*Build Num:* ${env.BUILD_NUMBER}\n*Test Host:* ${env.SERVICE_HOST_ENDPOINT}\n*Test Result:* :green_light:Passed\n*Test Duration:* ${currentBuild.durationString}\n*Test Report:* ${env.BUILD_URL}allure/\n*Docker Image Version:* ${env.Docker_Image_Version}\n*Service Version:* ${env.SERVICE_GIT_PR}-${env.SERVICE_GIT_COMMIT}-${env.SERVICE_GIT_TAG}\n*Test Case Version:* ${env.GIT_BRANCH}-${env.GIT_COMMIT}\n*Integration Test Skipped:* ${env.SKIP_INT_CASE}"
                    )
                }
            }
        }
        unstable {
            script {
                if (TEST_TYPE == 'ci') {
                    slackSend (
                        channel: '#ssp-ci',
                        teamDomain: 'vungle',
                        tokenCredentialId: 'jenkins_slack_token',
                        color: '#F8DE00',
                        message: "*Test Job:* ${env.JOB_NAME}\n*Build Num:* ${env.BUILD_NUMBER}\n*Test Host:* ${env.SERVICE_HOST_ENDPOINT}\n*Test Result:* :red_light:Failed\n*Test Duration:* ${currentBuild.durationString}\n*Test Report:* ${env.BUILD_URL}allure/\n*Docker Image Version:* ${env.Docker_Image_Version}\n*Service Version:* ${env.SERVICE_GIT_PR}-${env.SERVICE_GIT_COMMIT}-${env.SERVICE_GIT_TAG}\n*Test Case Version:* ${env.GIT_BRANCH}-${env.GIT_COMMIT}\n*Integration Test Skipped:* ${env.SKIP_INT_CASE}"
                    )
                } else if (TEST_TYPE == 'regression') {
                    slackSend (
                        channel: '#jaeger-feed',
                        teamDomain: 'vungle',
                        tokenCredentialId: 'platform_ci_test_slack_token',
                        color: '#F8DE00',
                        message: "*Test Job:* ${env.JOB_NAME}\n*Build Num:* ${env.BUILD_NUMBER}\n*Test Host:* ${env.SERVICE_HOST_ENDPOINT}\n*Test Result:* :red_light:Failed\n*Test Duration:* ${currentBuild.durationString}\n*Test Report:* ${env.BUILD_URL}allure/\n*Docker Image Version:* ${env.Docker_Image_Version}\n*Service Version:* ${env.SERVICE_GIT_PR}-${env.SERVICE_GIT_COMMIT}-${env.SERVICE_GIT_TAG}\n*Test Case Version:* ${env.GIT_BRANCH}-${env.GIT_COMMIT}\n*Integration Test Skipped:* ${env.SKIP_INT_CASE}"
                    )
                }
            }
        }
        failure {
            script {
                if (TEST_TYPE == 'ci') {
                    slackSend (
                        channel: '#ssp-ci',
                        teamDomain: 'vungle',
                        tokenCredentialId: 'jenkins_slack_token',
                        color: '#FF0000',
                        message: "The job ${env.JOB_NAME} is broken, Please check the reason. (${env.BUILD_URL}allure/)"
                    )
                } else if (TEST_TYPE == 'regression') {
                    slackSend (
                        channel: '#jaeger-feed',
                        teamDomain: 'vungle',
                        tokenCredentialId: 'platform_ci_test_slack_token',
                        color: '#FF0000',
                        message: "The job ${env.JOB_NAME} is broken, Please check the reason. (${env.BUILD_URL}allure/)"
                    )
                }
            }
        }
    }
}