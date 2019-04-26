# Contributor Covenant Code of Conduct

## Our Pledge

In the interest of fostering an open and welcoming environment, we as
contributors and maintainers pledge to making participation in our project and
our community a harassment-free experience for everyone, regardless of age, body
size, disability, ethnicity, sex characteristics, gender identity and expression,
level of experience, education, socio-economic status, nationality, personal
appearance, race, religion, or sexual identity and orientation.

## Our Standards

Examples of behavior that contributes to creating a positive environment
include:

* Using welcoming and inclusive language
* Being respectful of differing viewpoints and experiences
* Gracefully accepting constructive criticism
* Focusing on what is best for the community
* Showing empathy towards other community members

Examples of unacceptable behavior by participants include:

* The use of sexualized language or imagery and unwelcome sexual attention or
  advances
* Trolling, insulting/derogatory comments, and personal or political attacks
* Public or private harassment
* Publishing others' private information, such as a physical or electronic
  address, without explicit permission
* Other conduct which could reasonably be considered inappropriate in a
  professional setting

## Our Responsibilities

Project maintainers are responsible for clarifying the standards of acceptable
behavior and are expected to take appropriate and fair corrective action in
response to any instances of unacceptable behavior.

Project maintainers have the right and responsibility to remove, edit, or
reject comments, commits, code, wiki edits, issues, and other contributions
that are not aligned to this Code of Conduct, or to ban temporarily or
permanently any contributor for other behaviors that they deem inappropriate,
threatening, offensive, or harmful.

## Scope

This Code of Conduct applies both within project spaces and in public spaces
when an individual is representing the project or its community. Examples of
representing a project or community include using an official project e-mail
address, posting via an official social media account, or acting as an appointed
representative at an online or offline event. Representation of a project may be
further defined and clarified by project maintainers.

## Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be
reported by contacting the project team responsible teachers.
All complaints will be reviewed and investigated and will result in a response that
is deemed necessary and appropriate to the circumstances. The project team is
obligated to maintain confidentiality with regard to the reporter of an incident.
Further details of specific enforcement policies may be posted separately.

Project maintainers who do not follow or enforce the Code of Conduct in good
faith may face temporary or permanent repercussions as determined by other
members of the project's leadership.

## To Contribute

In order to contribute to the current project, the potential contributor must comply with the following rules otherwise its proposed changes may be denied and result in lost of time for everyone.

 1. Commit messages have to respect the following template:

    ```{bash}
    {Verb} reason for changes
    ```

    - Possible example of commit verbs are [Fix, Add, Implement]
    - The commit message must be fluidly read as a following of the phrase "This commit should"
        - This commit should <Add documentation for reading qrCodes>
    - The commit message must also include a reason for the changes to be necessary which is simply to explain what are the modification brought by this commit and why/how these modifications are useful to the development of the application. Simply citing an acception criteria or desired feature along with a general statement about what have changed is considered like good enough.
1. This repository follow the following git-flow workflow.
    - The repository will use 2 different types of branches
        - master
          : production level - should never commit directly on this branch.
        - feature/{featureName}
          : unstable, some commits may generate error on build - will be used by developers to create new features and resolve issues.
1. The team members engage to review pull requests within 24 hours.
1. For a pull request to be accepted, at least 1 developers must accept the pull request.
1. All source code must follow the PEP8 with typing.
1. The code base must be unit tested thoroughly.

    > A good way to achieve this is to use a TDD approach.

1. The name of the unit tests must follow the given_when_then standard.

    > When there is nothing in particular to be written as a given clause (other than the class name itself), the given clause should be omitted from the test name.

1. Mutator methods having arguments homonym in reference to class attribute must be prefixed by lowercase p. This also apply to constructor method.

    ```{python}
    mutatorMethod(attributeName) {
      this.attributeName = attributeName
    }
    ```

1. The feature branches should be named as ``feature/{feature_name}``. The ``{feature_name}`` can easily be identified using the trello of the project under the appropriate board of the [team page](https://trello.com/team7design32019).

## Attribution

This Code of Conduct is adapted from the [Contributor Covenant][homepage], version 1.4,
available at https://www.contributor-covenant.org/version/1/4/code-of-conduct.html

[homepage]: https://www.contributor-covenant.org
