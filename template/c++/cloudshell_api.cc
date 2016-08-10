#include "cloudshell_api.h"

namespace qualisystems {
    CloudShellAPISession::CloudShellAPISession(const std::string& host, const std::string& username,
                                 const std::string& password, const std::string& domain,
                                 const std::string& timezone = 'UTC', const std::string& datetime_format = 'MM/dd/yyyy HH:mm') {

    }

    CloudShellAPISession::~CloudShellAPISession();

// begin API

    std::string CloudShellAPISession::Logon(const std::string& username, const std::string& password,
                                            const std::string& domainName) {
        /**
            Logs in a user. If no user is specified, this method logs in the current user. If no domain is specified,
            this method logs the user in to the global (default) domain.

            :param username: Username to logon with.
            :param password: Specify the user's login password.
            :param domainName: Specify the name of the domain. If no domain is specified, it logs the user in to the global.
        **/
        return self.generateAPIRequest({{"username", convertToStr(username)}, {"password", convertToStr(password)}, {"domainName", convertToStr(domainName)}})
    }
}