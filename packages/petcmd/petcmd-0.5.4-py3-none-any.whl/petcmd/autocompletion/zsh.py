
ZSH_AUTOCOMPLETE_TEMPLATE = """
#compdef {alias}

local -a completions
completions=("${{(@f)$({alias} --shell-completion "$((CURRENT-2))" "${{words[@]:1}}")}}")
completions=(${{completions:#}})

if [[ "$completions[1]" == "__files__" ]]; then
  _files && return 0
  return 1
fi

if (( ${{#completions}} == 0 )); then
  return 1
fi

compadd -V unsorted -a completions
return 0
""".lstrip()
