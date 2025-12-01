## Why
Currently, the search functionality (-s) only supports Exa API key configuration through environment variables (EXA_API_KEY). This creates friction for users who want to use the search feature without configuring environment variables, especially for one-time usage or when working across different environments.

## What Changes
- Add CLI parameter --exa-api-key to allow passing Exa API key directly
- Modify search functionality to check CLI parameter first, then environment variable
- Update error messages to guide users on both configuration options
- Maintain backward compatibility with existing EXA_API_KEY environment variable

## Impact
- Affected specs: url-lookup capability (modify existing implementation)
- Affected code: argument parsing and Exa API key verification logic
- User experience: More flexible API key configuration options
- No breaking changes - existing environment variable method continues to work