export default defineAppConfig({
    ui: {
        formField: {
            slots: {
                root: '',
                wrapper: '',
                labelWrapper: 'flex content-center items-center justify-between',
                label: 'block font-semibold text-(--ui-text)',
                container: 'mt-2 relative',
                description: 'text-(--ui-text-muted)',
                error: 'mt-2 text-(--ui-error)',
                hint: 'text-(--ui-text-muted)',
                help: 'mt-2 text-(--ui-text-muted)'
            },
            variants: {
                size: {
                    xs: {
                        root: 'text-xs'
                    },
                    sm: {
                        root: 'text-xs'
                    },
                    md: {
                        root: 'text-sm'
                    },
                    lg: {
                        root: 'text-sm'
                    },
                    xl: {
                        root: 'text-base'
                    }
                },
                required: {
                    true: {
                        label: "after:content-['*'] after:ms-0.5 after:text-(--ui-error)"
                    }
                }
            },
            defaultVariants: {
                size: 'md'
            }
        },
        tabs: {
            slots: {
                root: 'flex items-center gap-2',
                list: 'relative flex p-1 group',
                indicator: 'absolute transition-[translate,width] duration-200',
                trigger:
                    'cursor-pointer group relative inline-flex items-center shrink-0 min-w-0 data-[state=inactive]:text-(--ui-text-muted) hover:data-[state=inactive]:not-disabled:text-(--ui-text) font-medium rounded-[calc(var(--ui-radius)*1.5)] disabled:cursor-not-allowed disabled:opacity-75 transition-colors',
                content: 'focus:outline-none w-full',
                leadingIcon: 'shrink-0',
                leadingAvatar: 'shrink-0',
                leadingAvatarSize: '',
                label: 'truncate'
            },
            variants: {
                color: {
                    primary: '',
                    secondary: '',
                    success: '',
                    info: '',
                    warning: '',
                    error: '',
                    neutral: ''
                },
                variant: {
                    pill: {
                        list: 'bg-(--ui-bg-elevated) rounded-[calc(var(--ui-radius)*2)]',
                        trigger: 'flex-1 w-full',
                        indicator: 'rounded-[calc(var(--ui-radius)*1.5)] shadow-xs'
                    },
                    link: {
                        list: 'border-(--ui-border)',
                        indicator: 'rounded-full'
                    }
                },
                orientation: {
                    horizontal: {
                        root: 'flex-col',
                        list: 'w-full',
                        indicator:
                            'left-0 w-(--reka-tabs-indicator-size) translate-x-(--reka-tabs-indicator-position)',
                        trigger: 'justify-center'
                    },
                    vertical: {
                        list: 'flex-col',
                        indicator:
                            'top-0 h-(--reka-tabs-indicator-size) translate-y-(--reka-tabs-indicator-position)'
                    }
                },
                size: {
                    xs: {
                        trigger: 'px-2 py-1 text-xs gap-1',
                        leadingIcon: 'size-4',
                        leadingAvatarSize: '3xs'
                    },
                    sm: {
                        trigger: 'px-2.5 py-1.5 text-xs gap-1.5',
                        leadingIcon: 'size-4',
                        leadingAvatarSize: '3xs'
                    },
                    md: {
                        trigger: 'px-0 py-1.5 text-sm gap-1.5',
                        leadingIcon: 'size-5',
                        leadingAvatarSize: '2xs'
                    },
                    lg: {
                        trigger: 'px-0 py-2 text-sm gap-2',
                        leadingIcon: 'size-5',
                        leadingAvatarSize: '2xs'
                    },
                    xl: {
                        trigger: 'px-3 py-2 text-base gap-2',
                        leadingIcon: 'size-6',
                        leadingAvatarSize: 'xs'
                    }
                }
            },
            compoundVariants: [
                {
                    orientation: 'horizontal',
                    variant: 'pill',
                    class: {
                        indicator: 'inset-y-1'
                    }
                },
                {
                    orientation: 'horizontal',
                    variant: 'link',
                    class: {
                        list: 'border-b-2 -mb-px gap-5',
                        indicator: '-bottom-px h-1'
                    }
                },
                {
                    orientation: 'vertical',
                    variant: 'pill',
                    class: {
                        indicator: 'inset-x-1',
                        list: 'items-center'
                    }
                },
                {
                    orientation: 'vertical',
                    variant: 'link',
                    class: {
                        list: 'border-s -ms-px',
                        indicator: '-start-px w-px'
                    }
                },
                {
                    color: 'primary',
                    variant: 'pill',
                    class: {
                        indicator: 'bg-(--ui-primary)',
                        trigger:
                            'data-[state=active]:text-(--ui-bg) focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-(--ui-primary)'
                    }
                },
                {
                    color: 'neutral',
                    variant: 'pill',
                    class: {
                        indicator: 'bg-(--ui-bg-inverted)',
                        trigger:
                            'data-[state=active]:text-(--ui-bg) focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-(--ui-border-inverted)'
                    }
                },
                {
                    color: 'primary',
                    variant: 'link',
                    class: {
                        indicator: 'bg-(--ui-primary)',
                        trigger:
                            'data-[state=active]:text-(--ui-primary) focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-(--ui-primary)'
                    }
                },
                {
                    color: 'neutral',
                    variant: 'link',
                    class: {
                        indicator: 'bg-(--ui-bg-inverted)',
                        trigger:
                            'data-[state=active]:text-(--ui-text-highlighted) focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-(--ui-border-inverted)'
                    }
                }
            ],
            defaultVariants: {
                color: 'primary',
                variant: 'pill',
                size: 'md'
            }
        },

        input: {
            slots: {
                root: 'relative inline-flex items-center',
                base: 'w-full rounded-[calc(var(--ui-radius)*1.5)] border-0 placeholder:text-(--ui-text-dimmed) focus:outline-none disabled:cursor-not-allowed disabled:opacity-75 transition-colors',
                leading: 'absolute inset-y-0 start-0 flex items-center',
                leadingIcon: 'shrink-0 text-(--ui-text-dimmed)',
                leadingAvatar: 'shrink-0',
                leadingAvatarSize: '',
                trailing: 'absolute inset-y-0 end-0 flex items-center',
                trailingIcon: 'shrink-0 text-(--ui-text-dimmed)'
            },
            variants: {
                buttonGroup: {
                    horizontal: {
                        root: 'group',
                        base: 'group-not-only:group-first:rounded-e-none group-not-only:group-last:rounded-s-none group-not-last:group-not-first:rounded-none'
                    },
                    vertical: {
                        root: 'group',
                        base: 'group-not-only:group-first:rounded-b-none group-not-only:group-last:rounded-t-none group-not-last:group-not-first:rounded-none'
                    }
                },
                size: {
                    xs: {
                        base: 'px-2 py-1 text-xs gap-1',
                        leading: 'ps-2',
                        trailing: 'pe-2',
                        leadingIcon: 'size-4',
                        leadingAvatarSize: '3xs',
                        trailingIcon: 'size-4'
                    },
                    sm: {
                        base: 'px-2.5 py-1.5 text-xs gap-1.5',
                        leading: 'ps-2.5',
                        trailing: 'pe-2.5',
                        leadingIcon: 'size-4',
                        leadingAvatarSize: '3xs',
                        trailingIcon: 'size-4'
                    },
                    md: {
                        base: 'px-2.5 py-1.5 text-sm gap-1.5',
                        leading: 'ps-2.5',
                        trailing: 'pe-2.5',
                        leadingIcon: 'size-5',
                        leadingAvatarSize: '2xs',
                        trailingIcon: 'size-5'
                    },
                    lg: {
                        base: 'px-3 py-2 text-sm gap-2',
                        leading: 'ps-3',
                        trailing: 'pe-3',
                        leadingIcon: 'size-5',
                        leadingAvatarSize: '2xs',
                        trailingIcon: 'size-5'
                    },
                    xl: {
                        base: 'py-3.5 px-5 leading-6 text-sm font-medium gap-2',
                        leading: 'ps-3',
                        trailing: 'pe-3',
                        leadingIcon: 'size-6',
                        leadingAvatarSize: 'xs',
                        trailingIcon: 'size-6'
                    }
                },
                variant: {
                    outline:
                        'text-(--ui-text-highlighted) bg-(--ui-bg) ring ring-inset ring-(--ui-border-accented)',
                    soft: 'text-(--ui-text-highlighted) bg-(--ui-bg-elevated)/50 hover:bg-(--ui-bg-elevated) focus:bg-(--ui-bg-elevated) disabled:bg-(--ui-bg-elevated)/50',
                    subtle: 'text-(--ui-text-highlighted) bg-(--ui-bg-elevated) ring ring-inset ring-(--ui-border-accented)',
                    ghost: 'text-(--ui-text-highlighted) bg-transparent hover:bg-(--ui-bg-elevated) focus:bg-(--ui-bg-elevated) disabled:bg-transparent dark:disabled:bg-transparent',
                    none: 'text-(--ui-text-highlighted) bg-transparent'
                },
                color: {
                    primary: '',
                    secondary: '',
                    success: '',
                    info: '',
                    warning: '',
                    error: '',
                    neutral: ''
                },
                leading: {
                    true: ''
                },
                trailing: {
                    true: ''
                },
                loading: {
                    true: ''
                },
                highlight: {
                    true: ''
                },
                type: {
                    file: 'file:me-1.5 file:font-medium file:text-(--ui-text-muted) file:outline-none'
                }
            },
            compoundVariants: [
                {
                    color: 'primary',
                    variant: ['outline', 'subtle'],
                    class: 'focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-(--ui-primary)'
                },
                {
                    color: 'primary',
                    highlight: true,
                    class: 'ring ring-inset ring-(--ui-primary)'
                },
                {
                    color: 'neutral',
                    variant: ['outline', 'subtle'],
                    class: 'focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-(--ui-border-inverted)'
                },
                {
                    color: 'neutral',
                    highlight: true,
                    class: 'ring ring-inset ring-(--ui-border-inverted)'
                },
                {
                    leading: true,
                    size: 'xs',
                    class: 'ps-7'
                },
                {
                    leading: true,
                    size: 'sm',
                    class: 'ps-8'
                },
                {
                    leading: true,
                    size: 'md',
                    class: 'ps-9'
                },
                {
                    leading: true,
                    size: 'lg',
                    class: 'ps-10'
                },
                {
                    leading: true,
                    size: 'xl',
                    class: 'ps-11'
                },
                {
                    trailing: true,
                    size: 'xs',
                    class: 'pe-7'
                },
                {
                    trailing: true,
                    size: 'sm',
                    class: 'pe-8'
                },
                {
                    trailing: true,
                    size: 'md',
                    class: 'pe-9'
                },
                {
                    trailing: true,
                    size: 'lg',
                    class: 'pe-10'
                },
                {
                    trailing: true,
                    size: 'xl',
                    class: 'pe-11'
                },
                {
                    loading: true,
                    leading: true,
                    class: {
                        leadingIcon: 'animate-spin'
                    }
                },
                {
                    loading: true,
                    leading: false,
                    trailing: true,
                    class: {
                        trailingIcon: 'animate-spin'
                    }
                }
            ],
            defaultVariants: {
                size: 'md',
                color: 'primary',
                variant: 'outline'
            }
        },

        button: {
            slots: {
                base: 'cursor-pointer rounded-[calc(var(--ui-radius)*1.5)] font-medium inline-flex items-center focus:outline-hidden disabled:cursor-not-allowed aria-disabled:cursor-not-allowed disabled:opacity-75 aria-disabled:opacity-75 transition-colors',
                label: 'truncate',
                leadingIcon: 'shrink-0',
                leadingAvatar: 'shrink-0',
                leadingAvatarSize: '',
                trailingIcon: 'shrink-0'
            },
            variants: {
                buttonGroup: {
                    horizontal:
                        'not-only:first:rounded-e-none not-only:last:rounded-s-none not-last:not-first:rounded-none',
                    vertical:
                        'not-only:first:rounded-b-none not-only:last:rounded-t-none not-last:not-first:rounded-none'
                },
                color: {
                    primary: '',
                    secondary: '',
                    success: '',
                    info: '',
                    warning: '',
                    error: '',
                    neutral: ''
                },
                variant: {
                    solid: '',
                    outline: '',
                    soft: '',
                    subtle: '',
                    ghost: '',
                    link: ''
                },
                size: {
                    xs: {
                        base: 'px-2 py-1 text-xs gap-1',
                        leadingIcon: 'size-4',
                        leadingAvatarSize: '3xs',
                        trailingIcon: 'size-4'
                    },
                    sm: {
                        base: 'px-2.5 py-1.5 text-xs gap-1.5',
                        leadingIcon: 'size-4',
                        leadingAvatarSize: '3xs',
                        trailingIcon: 'size-4'
                    },
                    md: {
                        base: 'px-2.5 py-1.5 text-sm gap-1.5',
                        leadingIcon: 'size-5',
                        leadingAvatarSize: '2xs',
                        trailingIcon: 'size-5'
                    },
                    lg: {
                        base: 'px-3 py-2 text-sm gap-2',
                        leadingIcon: 'size-5',
                        leadingAvatarSize: '2xs',
                        trailingIcon: 'size-5'
                    },
                    xl: {
                        base: 'px-3 py-2 text-base gap-2',
                        leadingIcon: 'size-6',
                        leadingAvatarSize: 'xs',
                        trailingIcon: 'size-6'
                    }
                },
                block: {
                    true: {
                        base: 'w-full justify-center',
                        trailingIcon: 'ms-auto'
                    }
                },
                square: {
                    true: ''
                },
                leading: {
                    true: ''
                },
                trailing: {
                    true: ''
                },
                loading: {
                    true: ''
                },
                active: {
                    true: {
                        base: ''
                    },
                    false: {
                        base: ''
                    }
                }
            },
            compoundVariants: [
                {
                    color: 'primary',
                    variant: 'solid',
                    class: 'text-(--ui-bg) bg-(--ui-primary) hover:bg-(--ui-primary)/75 disabled:bg-(--ui-primary) aria-disabled:bg-(--ui-primary) focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-(--ui-primary)'
                },
                {
                    color: 'primary',
                    variant: 'outline',
                    class: 'ring ring-inset ring-(--ui-primary)/50 text-(--ui-primary) hover:bg-(--ui-primary)/10 disabled:bg-transparent aria-disabled:bg-transparent dark:disabled:bg-transparent dark:aria-disabled:bg-transparent focus-visible:ring-2 focus-visible:ring-(--ui-primary)'
                },
                {
                    color: 'primary',
                    variant: 'soft',
                    class: 'text-(--ui-primary) bg-(--ui-primary)/10 hover:bg-(--ui-primary)/15 focus-visible:bg-(--ui-primary)/15 disabled:bg-(--ui-primary)/10 aria-disabled:bg-(--ui-primary)/10'
                },
                {
                    color: 'primary',
                    variant: 'subtle',
                    class: 'text-(--ui-primary) ring ring-inset ring-(--ui-primary)/25 bg-(--ui-primary)/10 hover:bg-(--ui-primary)/15 disabled:bg-(--ui-primary)/10 aria-disabled:bg-(--ui-primary)/10 focus-visible:ring-2 focus-visible:ring-(--ui-primary)'
                },
                {
                    color: 'primary',
                    variant: 'ghost',
                    class: 'text-(--ui-primary) hover:bg-(--ui-primary)/10 focus-visible:bg-(--ui-primary)/10 disabled:bg-transparent aria-disabled:bg-transparent dark:disabled:bg-transparent dark:aria-disabled:bg-transparent'
                },
                {
                    color: 'primary',
                    variant: 'link',
                    class: 'text-(--ui-primary) hover:text-(--ui-primary)/75 disabled:text-(--ui-primary) aria-disabled:text-(--ui-primary) focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-(--ui-primary)'
                },
                {
                    color: 'neutral',
                    variant: 'solid',
                    class: 'text-(--ui-bg) bg-(--ui-bg-inverted) hover:bg-(--ui-bg-inverted)/90 disabled:bg-(--ui-bg-inverted) aria-disabled:bg-(--ui-bg-inverted) focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-(--ui-border-inverted)'
                },
                {
                    color: 'neutral',
                    variant: 'outline',
                    class: 'ring ring-inset ring-(--ui-border-accented) text-(--ui-text) bg-(--ui-bg) hover:bg-(--ui-bg-elevated) disabled:bg-(--ui-bg) aria-disabled:bg-(--ui-bg) focus-visible:ring-2 focus-visible:ring-(--ui-border-inverted)'
                },
                {
                    color: 'neutral',
                    variant: 'soft',
                    class: 'text-(--ui-text) bg-(--ui-bg-elevated) hover:bg-(--ui-bg-accented)/75 focus-visible:bg-(--ui-bg-accented)/75 disabled:bg-(--ui-bg-elevated) aria-disabled:bg-(--ui-bg-elevated)'
                },
                {
                    color: 'neutral',
                    variant: 'subtle',
                    class: 'ring ring-inset ring-(--ui-border-accented) text-(--ui-text) bg-(--ui-bg-elevated) hover:bg-(--ui-bg-accented)/75 disabled:bg-(--ui-bg-elevated) aria-disabled:bg-(--ui-bg-elevated) focus-visible:ring-2 focus-visible:ring-(--ui-border-inverted)'
                },
                {
                    color: 'neutral',
                    variant: 'ghost',
                    class: 'text-(--ui-text) hover:bg-(--ui-bg-elevated) focus-visible:bg-(--ui-bg-elevated) hover:disabled:bg-transparent dark:hover:disabled:bg-transparent hover:aria-disabled:bg-transparent dark:hover:aria-disabled:bg-transparent'
                },
                {
                    color: 'neutral',
                    variant: 'link',
                    class: 'text-(--ui-text-muted) hover:text-(--ui-text) disabled:text-(--ui-text-muted) aria-disabled:text-(--ui-text-muted) focus-visible:ring-inset focus-visible:ring-2 focus-visible:ring-(--ui-border-inverted)'
                },
                {
                    size: 'xs',
                    square: true,
                    class: 'p-1'
                },
                {
                    size: 'sm',
                    square: true,
                    class: 'p-1.5'
                },
                {
                    size: 'md',
                    square: true,
                    class: 'p-1.5'
                },
                {
                    size: 'lg',
                    square: true,
                    class: 'p-2'
                },
                {
                    size: 'xl',
                    square: true,
                    class: 'p-2'
                },
                {
                    loading: true,
                    leading: true,
                    class: {
                        leadingIcon: 'animate-spin'
                    }
                },
                {
                    loading: true,
                    leading: false,
                    trailing: true,
                    class: {
                        trailingIcon: 'animate-spin'
                    }
                }
            ],
            defaultVariants: {
                color: 'primary',
                variant: 'solid',
                size: 'md'
            }
        },
        select: {
            slots: {
                base: 'relative group rounded-[calc(var(--ui-radius)*1.5)] inline-flex items-center focus:outline-none disabled:cursor-not-allowed disabled:opacity-75 transition-colors',
                leading: 'absolute inset-y-0 start-0 flex items-center',
                leadingIcon: 'shrink-0 text-(--ui-text-dimmed)',
                leadingAvatar: 'shrink-0',
                leadingAvatarSize: '',
                trailing: 'absolute inset-y-0 end-0 flex items-center',
                trailingIcon: 'shrink-0 text-(--ui-text-dimmed)',
                value: 'truncate pointer-events-none',
                placeholder: 'truncate text-(--ui-text-dimmed)',
                arrow: 'fill-(--ui-border)',
                content:
                    'max-h-60 w-(--reka-popper-anchor-width) bg-(--ui-bg) shadow-lg rounded-[calc(var(--ui-radius)*1.5)] ring ring-(--ui-border) overflow-hidden data-[state=open]:animate-[scale-in_100ms_ease-out] data-[state=closed]:animate-[scale-out_100ms_ease-in] pointer-events-auto',
                viewport: 'divide-y divide-(--ui-border) scroll-py-1',
                group: 'p-1 isolate',
                empty: 'py-2 text-center text-sm text-(--ui-text-muted)',
                label: 'font-semibold text-(--ui-text-highlighted)',
                separator: '-mx-1 my-1 h-px bg-(--ui-border)',
                item: [
                    'group relative w-full flex items-center select-none outline-none before:absolute before:z-[-1] before:inset-px before:rounded-[calc(var(--ui-radius)*1.5)] data-disabled:cursor-not-allowed data-disabled:opacity-75 text-(--ui-text) data-highlighted:text-(--ui-text-highlighted) data-highlighted:before:bg-(--ui-bg-elevated)/50',
                    'transition-colors before:transition-colors'
                ],
                itemLeadingIcon: [
                    'shrink-0 text-(--ui-text-dimmed) group-data-highlighted:text-(--ui-text)',
                    'transition-colors'
                ],
                itemLeadingAvatar: 'shrink-0',
                itemLeadingAvatarSize: '',
                itemLeadingChip: 'shrink-0',
                itemLeadingChipSize: '',
                itemTrailing: 'ms-auto inline-flex gap-1.5 items-center',
                itemTrailingIcon: 'shrink-0',
                itemLabel: 'truncate'
            },
            variants: {
                buttonGroup: {
                    horizontal:
                        'not-only:first:rounded-e-none not-only:last:rounded-s-none not-last:not-first:rounded-none',
                    vertical:
                        'not-only:first:rounded-b-none not-only:last:rounded-t-none not-last:not-first:rounded-none'
                },
                size: {
                    xs: {
                        base: 'px-2 py-1 text-xs gap-1',
                        leading: 'ps-2',
                        trailing: 'pe-2',
                        leadingIcon: 'size-4',
                        leadingAvatarSize: '3xs',
                        trailingIcon: 'size-4',
                        label: 'p-1 text-[10px]/3 gap-1',
                        item: 'p-1 text-xs gap-1',
                        itemLeadingIcon: 'size-4',
                        itemLeadingAvatarSize: '3xs',
                        itemLeadingChip: 'size-4',
                        itemLeadingChipSize: 'sm',
                        itemTrailingIcon: 'size-4'
                    },
                    sm: {
                        base: 'px-2.5 py-1.5 text-xs gap-1.5',
                        leading: 'ps-2.5',
                        trailing: 'pe-2.5',
                        leadingIcon: 'size-4',
                        leadingAvatarSize: '3xs',
                        trailingIcon: 'size-4',
                        label: 'p-1.5 text-[10px]/3 gap-1.5',
                        item: 'p-1.5 text-xs gap-1.5',
                        itemLeadingIcon: 'size-4',
                        itemLeadingAvatarSize: '3xs',
                        itemLeadingChip: 'size-4',
                        itemLeadingChipSize: 'sm',
                        itemTrailingIcon: 'size-4'
                    },
                    md: {
                        base: 'px-2.5 py-1.5 text-sm gap-1.5',
                        leading: 'ps-2.5',
                        trailing: 'pe-2.5',
                        leadingIcon: 'size-5',
                        leadingAvatarSize: '2xs',
                        trailingIcon: 'size-5',
                        label: 'p-1.5 text-xs gap-1.5',
                        item: 'p-1.5 text-sm gap-1.5',
                        itemLeadingIcon: 'size-5',
                        itemLeadingAvatarSize: '2xs',
                        itemLeadingChip: 'size-5',
                        itemLeadingChipSize: 'md',
                        itemTrailingIcon: 'size-5'
                    },
                    lg: {
                        base: 'px-3 py-2 text-sm gap-2',
                        leading: 'ps-3',
                        trailing: 'pe-3',
                        leadingIcon: 'size-5',
                        leadingAvatarSize: '2xs',
                        trailingIcon: 'size-5',
                        label: 'p-2 text-xs gap-2',
                        item: 'p-2 text-sm gap-2',
                        itemLeadingIcon: 'size-5',
                        itemLeadingAvatarSize: '2xs',
                        itemLeadingChip: 'size-5',
                        itemLeadingChipSize: 'md',
                        itemTrailingIcon: 'size-5'
                    },
                    xl: {
                        base: 'py-3.5 px-5 leading-6 text-sm font-medium gap-2',
                        leading: 'ps-3',
                        trailing: 'pe-3',
                        leadingIcon: 'size-6',
                        leadingAvatarSize: 'xs',
                        trailingIcon: 'size-6',
                        label: 'p-2 text-sm gap-2',
                        item: 'p-2 text-base gap-2',
                        itemLeadingIcon: 'size-6',
                        itemLeadingAvatarSize: 'xs',
                        itemLeadingChip: 'size-6',
                        itemLeadingChipSize: 'lg',
                        itemTrailingIcon: 'size-6'
                    }
                },
                variant: {
                    outline:
                        'text-(--ui-text-highlighted) bg-(--ui-bg) ring ring-inset ring-(--ui-border-accented)',
                    soft: 'text-(--ui-text-highlighted) bg-(--ui-bg-elevated)/50 hover:bg-(--ui-bg-elevated) focus:bg-(--ui-bg-elevated) disabled:bg-(--ui-bg-elevated)/50',
                    subtle: 'text-(--ui-text-highlighted) bg-(--ui-bg-elevated) ring ring-inset ring-(--ui-border-accented)',
                    ghost: 'text-(--ui-text-highlighted) bg-transparent hover:bg-(--ui-bg-elevated) focus:bg-(--ui-bg-elevated) disabled:bg-transparent dark:disabled:bg-transparent',
                    none: 'text-(--ui-text-highlighted) bg-transparent'
                },
                color: {
                    primary: '',
                    secondary: '',
                    success: '',
                    info: '',
                    warning: '',
                    error: '',
                    neutral: ''
                },
                leading: {
                    true: ''
                },
                trailing: {
                    true: ''
                },
                loading: {
                    true: ''
                },
                highlight: {
                    true: ''
                },
                type: {
                    file: 'file:me-1.5 file:font-medium file:text-(--ui-text-muted) file:outline-none'
                }
            },
            compoundVariants: [
                {
                    color: 'primary',
                    variant: ['outline', 'subtle'],
                    class: 'focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-(--ui-primary)'
                },
                {
                    color: 'primary',
                    highlight: true,
                    class: 'ring ring-inset ring-(--ui-primary)'
                },
                {
                    color: 'neutral',
                    variant: ['outline', 'subtle'],
                    class: 'focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-(--ui-border-inverted)'
                },
                {
                    color: 'neutral',
                    highlight: true,
                    class: 'ring ring-inset ring-(--ui-border-inverted)'
                },
                {
                    leading: true,
                    size: 'xs',
                    class: 'ps-7'
                },
                {
                    leading: true,
                    size: 'sm',
                    class: 'ps-8'
                },
                {
                    leading: true,
                    size: 'md',
                    class: 'ps-9'
                },
                {
                    leading: true,
                    size: 'lg',
                    class: 'ps-10'
                },
                {
                    leading: true,
                    size: 'xl',
                    class: 'ps-11'
                },
                {
                    trailing: true,
                    size: 'xs',
                    class: 'pe-7'
                },
                {
                    trailing: true,
                    size: 'sm',
                    class: 'pe-8'
                },
                {
                    trailing: true,
                    size: 'md',
                    class: 'pe-9'
                },
                {
                    trailing: true,
                    size: 'lg',
                    class: 'pe-10'
                },
                {
                    trailing: true,
                    size: 'xl',
                    class: 'pe-11'
                },
                {
                    loading: true,
                    leading: true,
                    class: {
                        leadingIcon: 'animate-spin'
                    }
                },
                {
                    loading: true,
                    leading: false,
                    trailing: true,
                    class: {
                        trailingIcon: 'animate-spin'
                    }
                }
            ],
            defaultVariants: {
                size: 'md',
                color: 'primary',
                variant: 'outline'
            }
        },
        accordion: {
            slots: {
                root: 'w-full gap-3.5 grid',
                item: 'bg-white rounded-xl flex flex-col p-4  border-b border-(--ui-border) last:border-b-0',
                header: 'flex',
                trigger:
                    'group flex-1 flex items-center gap-1.5 py-0 font-medium text-sm focus-visible:outline-(--ui-primary) min-w-0',
                content:
                    ' data-[state=open]:animate-[accordion-down_200ms_ease-out] data-[state=closed]:animate-[accordion-up_200ms_ease-out] overflow-hidden focus:outline-none',
                body: 'text-sm pb-3.5 ',
                leadingIcon: 'shrink-0 size-5',
                trailingIcon:
                    'shrink-0 size-5 ms-auto group-data-[state=open]:rotate-180 transition-transform duration-200',
                label: 'font-bold text-sm text-black text-start break-words'
            },
            variants: {
                disabled: {
                    true: {
                        trigger: 'cursor-not-allowed opacity-75'
                    }
                }
            }
        },
        checkbox: {
            slots: {
                root: 'relative flex items-start',
                container: 'flex items-center',
                base: 'rounded-sm ring ring-inset ring-accented overflow-hidden focus-visible:outline-2 focus-visible:outline-offset-2',
                indicator: 'flex items-center justify-center size-full text-inverted',
                icon: 'shrink-0 size-full',
                wrapper: 'w-full',
                label: 'block font-medium text-default',
                description: 'text-muted'
            },
            variants: {
                color: {
                    primary: {
                        base: 'focus-visible:outline-primary text-white',
                        indicator: 'bg-primary'
                    },
                    secondary: {
                        base: 'focus-visible:outline-secondary',
                        indicator: 'bg-secondary'
                    },
                    success: {
                        base: 'focus-visible:outline-success',
                        indicator: 'bg-success'
                    },
                    info: {
                        base: 'focus-visible:outline-info',
                        indicator: 'bg-info'
                    },
                    warning: {
                        base: 'focus-visible:outline-warning',
                        indicator: 'bg-warning'
                    },
                    error: {
                        base: 'focus-visible:outline-error',
                        indicator: 'bg-error'
                    },
                    neutral: {
                        base: 'focus-visible:outline-inverted',
                        indicator: 'bg-inverted'
                    }
                },
                variant: {
                    list: {
                        root: ''
                    },
                    card: {
                        root: 'border border-muted rounded-lg'
                    }
                },
                indicator: {
                    start: {
                        root: 'flex-row',
                        wrapper: 'ms-2'
                    },
                    end: {
                        root: 'flex-row-reverse',
                        wrapper: 'me-2'
                    },
                    hidden: {
                        base: 'sr-only',
                        wrapper: 'text-center'
                    }
                },
                size: {
                    xs: {
                        base: 'size-3',
                        container: 'h-4',
                        wrapper: 'text-xs'
                    },
                    sm: {
                        base: 'size-3.5',
                        container: 'h-4',
                        wrapper: 'text-xs'
                    },
                    md: {
                        base: 'size-4',
                        container: 'h-5',
                        wrapper: 'text-sm'
                    },
                    lg: {
                        base: 'size-4.5',
                        container: 'h-5',
                        wrapper: 'text-sm'
                    },
                    xl: {
                        base: 'size-5',
                        container: 'h-6',
                        wrapper: 'text-sm'
                    }
                },
                required: {
                    true: {
                        label: "after:content-['*'] after:ms-0.5 after:text-error"
                    }
                },
                disabled: {
                    true: {
                        base: 'cursor-not-allowed opacity-75',
                        label: 'cursor-not-allowed opacity-75',
                        description: 'cursor-not-allowed opacity-75'
                    }
                },
                checked: {
                    true: ''
                }
            },
            compoundVariants: [
                {
                    size: 'xs',
                    variant: 'card',
                    class: {
                        root: 'p-2.5'
                    }
                },
                {
                    size: 'sm',
                    variant: 'card',
                    class: {
                        root: 'p-3'
                    }
                },
                {
                    size: 'md',
                    variant: 'card',
                    class: {
                        root: 'p-3.5'
                    }
                },
                {
                    size: 'lg',
                    variant: 'card',
                    class: {
                        root: 'p-4'
                    }
                },
                {
                    size: 'xl',
                    variant: 'card',
                    class: {
                        root: 'p-4.5'
                    }
                },
                {
                    color: 'primary',
                    variant: 'card',
                    class: {
                        root: 'has-data-[state=checked]:border-primary text-white'
                    }
                },
                {
                    color: 'neutral',
                    variant: 'card',
                    class: {
                        root: 'has-data-[state=checked]:border-inverted'
                    }
                },
                {
                    variant: 'card',
                    disabled: true,
                    class: {
                        root: 'cursor-not-allowed opacity-75'
                    }
                }
            ],
            defaultVariants: {
                size: 'md',
                color: 'primary',
                variant: 'list',
                indicator: 'start'
            }
        },
        alert: {
            slots: {
                root: 'relative overflow-hidden w-full rounded-lg p-4 flex !items-center gap-2.5',
                wrapper: 'min-w-0 flex-1 flex flex-col',
                title: 'text-sm font-medium',
                description: 'text-sm opacity-90',
                icon: 'shrink-0 !size-8',
                avatar: 'shrink-0',
                avatarSize: '2xl',
                actions: 'flex flex-wrap gap-1.5 shrink-0',
                close: 'p-0'
            },
            variants: {
                color: {
                    primary: '',
                    secondary: '',
                    success: '',
                    info: '',
                    warning: '',
                    error: '',
                    neutral: ''
                },
                variant: {
                    solid: '',
                    outline: '',
                    soft: '',
                    subtle: ''
                },
                orientation: {
                    horizontal: {
                        root: 'items-center',
                        actions: 'items-center'
                    },
                    vertical: {
                        root: 'items-start',
                        actions: 'items-start mt-2.5'
                    }
                },
                title: {
                    true: {
                        description: 'mt-1'
                    }
                }
            },
            compoundVariants: [
                {
                    color: 'primary',
                    variant: 'solid',
                    class: {
                        root: 'bg-primary text-inverted'
                    }
                },
                {
                    color: 'primary',
                    variant: 'outline',
                    class: {
                        root: 'text-primary ring ring-inset ring-primary/25'
                    }
                },
                {
                    color: 'primary',
                    variant: 'soft',
                    class: {
                        root: 'bg-primary/10 text-primary'
                    }
                },
                {
                    color: 'primary',
                    variant: 'subtle',
                    class: {
                        root: 'bg-primary/10 text-primary ring ring-inset ring-primary/25'
                    }
                },
                {
                    color: 'info',
                    variant: 'subtle',
                    class: {
                        root: 'border-info-light-active bg-info-light text-info-normal-active'
                    }
                },
                {
                    color: 'neutral',
                    variant: 'solid',
                    class: {
                        root: 'text-inverted bg-inverted'
                    }
                },
                {
                    color: 'neutral',
                    variant: 'outline',
                    class: {
                        root: 'text-highlighted bg-default ring ring-inset ring-default'
                    }
                },
                {
                    color: 'neutral',
                    variant: 'soft',
                    class: {
                        root: 'text-highlighted bg-elevated/50'
                    }
                },
                {
                    color: 'neutral',
                    variant: 'subtle',
                    class: {
                        root: 'text-highlighted bg-elevated/50 ring ring-inset ring-accented'
                    }
                }
            ],
            defaultVariants: {
                color: 'primary',
                variant: 'solid'
            }
        }
    }
})
