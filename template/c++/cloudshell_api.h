#ifndef QUALISYSTEMS_CLOUDSHELL_API_CLOUDSHELL_API_H_
#define QUALISYSTEMS_CLOUDSHELL_API_CLOUDSHELL_API_H_

#include "common_cloudshell_api.h"

namespace qualisystems {
    class CloudShellAPISession : public CommonAPISession {
    public:
        CloudShellAPISession(const std::string& host, const std::string& username,
                             const std::string& password, const std::string& domain,
                             const std::string& timezone = 'UTC', const std::string& datetime_format = 'MM/dd/yyyy HH:mm');
        ~CloudShellAPISession();

    public:
// begin API

    protected:
        std::string hostname_;
        std::string url_;
    };
}

#endif